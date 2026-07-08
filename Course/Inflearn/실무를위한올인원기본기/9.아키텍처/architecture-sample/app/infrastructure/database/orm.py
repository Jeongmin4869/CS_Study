from peewee import *
import datetime

# DB 의 경로를동적으로 처리해줄 수 있음
db = SqliteDatabase(None, thread_safe=True)


class BaseModel(Model):
    class Meta:
        database = db


# 테이블을DB에 만들때 필요한 객체
class UserModel(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = "users"


# 테이블을DB에 만들때 필요한 객체
class ProductModel(BaseModel):
    name = CharField(null=False)
    price = IntegerField(null=False)

    class Meta:
        table_name = "products"
