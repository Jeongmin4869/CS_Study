from peewee import *
import datetime

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class UserModel(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = "users"
