from typing import Optional, Any
import asyncio
from faker import Faker
import aiosqlite, random
from hashlib import md5
from os import path, remove
from shutil import rmtree
from montydb import set_storage, MontyClient
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from data import users

class User(BaseModel):
    name: str
    username: str
    address: str
    email: str
    password: str
    contact: str

DB_FILENAME = 'podlodka'
app = FastAPI()

set_storage(repository=f'{DB_FILENAME}.nosql.db', storage='sqlite', use_bson=False)

# The `db_client` variable is creating a MontyDB client instance to interact with the MontyDB
# database. It is connecting to the specified database file (`f"{DB_FILENAME}.nosql.db"`) and
# configuring the client with certain settings like synchronous mode, automatic indexing, and busy
# timeout. This client instance is used to perform operations on the MontyDB database, such as
# inserting data from a SQL database during initialization (`init_nosql_db` function) and querying for
# users based on a username (`get_nosql_users` function).
# The `db_client` variable is creating a MontyClient instance to connect to the database specified by
# the `DB_FILENAME` variable. It is used to interact with the NoSQL database storage for the
# application. The `MontyClient` is configured with specific settings such as the database file name,
# synchronous mode, automatic indexing, and busy timeout. This client is then used to access and
# manipulate data in the NoSQL database within the application.
db_client = MontyClient(
        f"{DB_FILENAME}.nosql.db",
        synchronous=1,
        automatic_index=False,
        busy_timeout=5000
        )

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    usernames = [user.get('username') for user in users[2::]]
    return templates.TemplateResponse(
        request=request, name="home.html", context={"usernames": usernames}
    )

async def get_sql_db():
    db = await aiosqlite.connect(database=f'{DB_FILENAME}.sql.db')
    return db

async def init_sql_db():
    if path.isfile(f'{DB_FILENAME}.sql.db'):
        remove(f'{DB_FILENAME}.sql.db')

    db = await get_sql_db()
    await db.execute(
        '''
                    CREATE TABLE users ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        name TEXT NOT NULL,
                                        username TEXT NOT NULL,
                                        password TEXT NOT NULL,
                                        address TEXT NOT NULL,
                                        email TEXT NOT NULL,
                                        contact TEXT NOT NULL,
                                        flag TEXT NOT NULL
                                        );'''[1:]
    )
    await db.commit()
    # for _ in range(random.randint(5, 10)):
    for user in users:
        query = f'''
                    INSERT INTO users ( name,
                                        username,
                                        password,
                                        address,
                                        email,
                                        contact,
                                        flag
                                        )
                        VALUES (
                                    "{user.get("name")}",
                                    "{user.get("username")}",
                                    "{user.get("passwd")}",
                                    "{user.get("address")}",
                                    "{user.get("email")}",
                                    "{user.get("contact")}",
                                    "{user.get("flag")}"
                                );
                '''[1:-1]
        await db.execute(query)
        await db.commit()
    await db.close()
    return True

async def run_sql_query(query, commit=False):
    try:
        db = await get_sql_db()
        cursor = await db.execute(query)
        _data, data = await cursor.fetchall(), {}
        if commit:
            await db.commit()
        await cursor.close()
        await db.close()
        if len(_data) == 1:
            if len(_data[0]) == 1 and type(_data[0][0]) == int:
                return _data[0][0]
            _data = _data[0]
            data['id'] = _data[0]
            data['name'] = _data[1]
            data['username'] = _data[2]
            data['address'] = _data[4]
            data['email'] = _data[5]
            data['contact'] = _data[6]
            data['flag'] = _data[7]
            return data
        return {'users': _data}
    except KeyboardInterrupt:
        await init_db()
        return await run_sql_query(query)

async def init_nosql_db():
    if path.isdir(f'{DB_FILENAME}.nosql.db'):
        rmtree(f'{DB_FILENAME}.nosql.db')
    users = db_client.podlodka.users
    data = await run_sql_query('SELECT * FROM USERS;')
    for user in data['users']:
        users.insert_one({
            'id': user[0],
            'name': user[1],
            'username': user[2],
            'address': user[4],
            'email': user[5],
            'contact': user[6],
            'flag': user[7],
            })

async def init_db():
    await init_sql_db()
    await init_nosql_db()

def get_nosql_users(query):
    if len(query)!= 1 or 'username' not in query:
        return "Ошибка: В запросе должен быть только один ключ 'username'"

    users = db_client.podlodka.users
    user_data = tuple(users.find(query))
    for data in user_data: 
        data.pop('_id')
    if len(user_data) == 1: return user_data[0]
    return tuple(user_data)

@app.get('/find')
async def nosql_return_users_from_username(username: str):
    return get_nosql_users({'username': username})

@app.post('/find')
async def nosql_return_users(request: Request):
    query = await request.json()
    return get_nosql_users(query)


@app.post('/reset/{password}')
async def reset_database(password):
    if password != "supErSecretPasw0Rd__supErSecretPasw0Rd":
        return {'resp': 'false'}
    remove(f'{DB_FILENAME}.sql.db')
    await init_db()
    return {'resp': 'done'}

if __name__ == '__main__':
    asyncio.run(init_db())
    uvicorn.run('app:app', port=8888, reload=False)
