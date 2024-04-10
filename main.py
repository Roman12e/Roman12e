from fastapi import FastAPI
from pydantic import BaseModel
import aiosqlite
import uuid
import uvicorn
import aiosqlite
import asyncio


async def create_database():
    async with aiosqlite.connect('users.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users(
                         id TEXT,
                         name TEXT,
                         email TEXT,
                         password TEXT
        )""")

        await db.commit()


app = FastAPI()


class User(BaseModel):
    username: str
    email: str
    password: str


@app.post('/register')
async def get_user_data(user: User):
    async with aiosqlite.connect('users.db') as db:
        await db.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (str(uuid.uuid4()), user.username, user.email, user.password))
        await db.commit()

        data = await db.execute("SELECT * FROM users")
        res = await data.fetchall()
        print(res)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database())