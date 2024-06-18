import asyncio
import aiosqlite
from hashlib import md5
from os import path, remove
from shutil import rmtree
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
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


async def init_db():
    await init_sql_db()


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


@app.get('/select')
async def sql_return_users_from_username(username: str):
    resp = await run_sql_query(f'SELECT * FROM users WHERE username = "{username}";')
    return resp


@app.post('/reset/{password}')
async def reset_database(password):
    if password != "supErSecretPasw0Rd":
        return {'resp': 'false'}
    remove(f'{DB_FILENAME}.sql.db')
    await init_db()
    return {'resp': 'done'}


if __name__ == '__main__':
    asyncio.run(init_db())
    uvicorn.run('app:app', port=8888, reload=False)
