from fastapi import FastAPI
from routers import auth
from database import db
from models.user import User

app = FastAPI()

db.connect()
db.create_tables([User])

app.include_router(auth.router)

@app.get("/")
async def index():
    return "Hello World!"