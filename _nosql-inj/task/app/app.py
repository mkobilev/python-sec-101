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

class User(BaseModel):
    name: str
    username: str
    address: str
    email: str
    password: str
    contact: str

DB_FILENAME = 'vfapi'
app = FastAPI(
        title="vFastAPI",
        version="0.01a",
        description=__doc__,
        contact=author_info,
        license_info=__license__,
        redoc_url=False,
        docs_url=False
        )
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


async def init_nosql_db():
    if path.isdir(f'{DB_FILENAME}.nosql.db'):
        rmtree(f'{DB_FILENAME}.nosql.db')
    users = db_client.vfapi.users
    data = await run_sql_query('SELECT * FROM USERS;')
    for user in data['users']:
        users.insert_one({
            'id': user[0],
            'name': user[1],
            'username': user[2],
            'address': user[4],
            'email': user[5],
            'contact': user[6]
            })

async def init_db():
    await init_nosql_db()

def get_nosql_users(query):
    users = db_client.vfapi.users
    user_data = tuple(users.find(query))
    for data in user_data: data.pop('_id'); data.pop('password')
    if len(user_data) == 1: return user_data[0]
    return tuple(user_data)

@app.get('/find')
async def nosql_return_users_from_username(username: str):
    return get_nosql_users({'username': username})

@app.post('/find')
async def nosql_return_users(request: Request):
    query = await request.json()
    return get_nosql_users(query)

@app.delete('/user')
async def delete_user(username: Optional[str] = '', user: Optional[User] = None):
    if username:
        db_client.vfapi.users.delete_one({'username': username})
        await run_sql_query(f'DELETE FROM users WHERE username = "{username}";', commit=True)
        return {'resp': 'done'}
    elif user:
        db_client.vfapi.users.delete_one({'address': user.address})
        await run_sql_query(f'DELETE FROM users WHERE address = {user.address};', commit=True)
    return {'resp': '!done'}

@app.get('/reset')
def reset_page():
    return {'resp': 'Please issue a POST request to the same endpoint in order to actually reset the database.'}

@app.post('/reset')
async def reset_database():
    remove(f'{DB_FILENAME}.sql.db')
    rmtree(f'{DB_FILENAME}.nosql.db')
    await init_db()
    return {'resp': 'done'}


if __name__ == '__main__':
    asyncio.run(init_db()); __import__('uvicorn').run('app:app', port=8888, reload=False)
