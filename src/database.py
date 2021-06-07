from peewee import *
import psycopg2

db = PostgresqlDatabase('fastapi', user='rodrigo', password='root', autorollback=True)

class BaseModel(Model):
    class Meta:
        database = db


def get_db():
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()
    