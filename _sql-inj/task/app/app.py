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
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


class User(BaseModel):
    name: str
    username: str
    address: str
    email: str
    password: str
    contact: str

DB_FILENAME = 'vfapi'
app = FastAPI()
fake = Faker()

set_storage(
        repository=f'{DB_FILENAME}.nosql.db',
        storage='sqlite',
        use_bson=False
        )
db_client = MontyClient(
        f"{DB_FILENAME}.nosql.db",
        synchronous=1,
        automatic_index=False,
        busy_timeout=5000
        )

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/index", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

async def get_sql_db():
    db = await aiosqlite.connect(database=f'{DB_FILENAME}.sql.db')
    return db

async def init_sql_db():
    if path.isfile(f'{DB_FILENAME}.sql.db'):
        remove(f'{DB_FILENAME}.sql.db')
    db = await get_sql_db()
    await db.execute('''
CREATE TABLE users ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     username TEXT NOT NULL,
                     password TEXT NOT NULL,
                     address TEXT NOT NULL,
                     email TEXT NOT NULL,
                     contact TEXT NOT NULL
                     );'''[1:])
    await db.commit()
    for _ in range(random.randint(7, 84)):
        query = f'''
INSERT INTO users ( name,
                    username,
                    password,
                    address,
                    email,
                    contact
                    )
       VALUES (
                "{fake.name()}",
                "{fake.user_name()}",
                "{md5(fake.password().encode()).hexdigest()}",
                "{fake.address()}",
                "{fake.email()}",
                "{fake.phone_number()}"
            ) ;
'''[1:-1]
        await db.execute(query)
        await db.commit()
    await db.close()
    return True

async def init_db():
    await init_sql_db()

async def run_sql_query(query, commit=False):
    try:
        db = await get_sql_db()
        cursor = await db.execute(query)
        _data, data = await cursor.fetchall(), {}
        if commit: await db.commit()
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
            return data
        return {'users': _data}
    except KeyboardInterrupt as e:
    # except Exception as e:
        print(e)
        await init_db()
        return await run_sql_query(query)

# @app.get('/')
# def root():
#     return {'goto': '/docs'}

@app.get('/select')
async def sql_return_users_from_username(username: str):
    resp = await run_sql_query(f'SELECT * FROM users WHERE username = "{username}";')
    return resp

@app.put('/user')
async def put_user(user: User):
    user.password = md5(user.password.encode()).hexdigest()
    query = f'''
INSERT INTO users (
                    name,
                    username,
                    password,
                    address,
                    email,
                    contact
                ) VALUES ( 
                            "{user.name}",
                            "{user.username}",
                            "{user.password}",
                            "{user.address}",
                            "{user.email}",
                            "{user.contact}"
                            );
'''[1:-1]
    await run_sql_query(query, commit=True)
    _id = await run_sql_query('SELECT id from users ORDER BY ROWID DESC limit 1;')
    db_client.vfapi.users.insert_one({
        'id': _id,
        'name': user.name,
        'username': user.username,
        'password': user.password,
        'address': user.address,
        'email': user.email,
        'contact': user.contact
        })
    return {'resp': 'done'}


# @app.delete('/user')
# async def delete_user(username: Optional[str] = '', user: Optional[User] = None):
#     if username:
#         db_client.vfapi.users.delete_one({'username': username})
#         await run_sql_query(f'DELETE FROM users WHERE username = "{username}";', commit=True)
#         return {'resp': 'done'}
#     elif user:
#         db_client.vfapi.users.delete_one({'address': user.address})
#         await run_sql_query(f'DELETE FROM users WHERE address = {user.address};', commit=True)
#     return {'resp': '!done'}

@app.get('/reset')
def reset_page():
    return {'resp': 'Please issue a POST request to the same endpoint in order to actually reset the database.'}

@app.post('/reset')
async def reset_database():
    remove(f'{DB_FILENAME}.sql.db')
    await init_db()
    return {'resp': 'done'}

if __name__ == '__main__':
    asyncio.run(init_db()); __import__('uvicorn').run('app:app', port=8888, reload=False)
