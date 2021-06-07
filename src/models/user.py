from enum import unique
from peewee import *
from database import db

class User(Model):
    class Meta:
        database = db
    username = CharField(unique=True)
    password = CharField()
