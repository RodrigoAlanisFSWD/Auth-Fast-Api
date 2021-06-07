from copy import Error
from fastapi import APIRouter
from fastapi.param_functions import Depends
from peewee import DoesNotExist, IntegrityError  
from models.http import UserRequest   
from models.user import User
from bcrypt import *
import jwt
from database import db

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(user: UserRequest):
    try:
        salt = gensalt()
        hash = hashpw(user.password.encode('utf-8'), salt)
        password = hash.decode('utf-8')

        newUser = User.create(username=user.username,password=password)

        print(newUser.id)
        token = jwt.encode({"id": newUser.id}, "secret", algorithm='HS256')

        return {
                "res": "SUCCESS",
                "auth": True,
                "token": token
            }
    except IntegrityError:
        return {
                "res": "Username Already Taken",
                "auth": False,
                "token": ""
            }

@router.post("/login")
def login(user: UserRequest):
    try:
        find = User.get(User.username == user.username)
        verify = checkpw(user.password.encode('utf-8'), find.password.encode('utf-8'))

        if not verify:
            return {
                "res": "The Password Is Invalid",
                "auth": False,
                "token": ""
            }
        token = jwt.encode({"id": find.id}, "secret", algorithm='HS256')

        return {
                "res": "SUCCESS",
                "auth": True,
                "token": token
            }
    except DoesNotExist:
        return {
                "res": "User Dont Exists With This Username",
                "auth": False,
                "token": ""
            }