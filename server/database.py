import datetime
from peewee import *

db = SqliteDatabase('dev.db')


class BaseModel(Model):
    class Meta:
        database = db


class Position(BaseModel):
    map_x = DoubleField()
    map_y = DoubleField()
    angle = DoubleField()


class Bus(BaseModel):
    name = CharField(primary_key=True)


class OrderPosition(BaseModel):
    order = IntField()
    position = ForeignKey(Position)


class Assignment(BaseModel):
    date = DateField()
    bus = ForeignKeyField(Bus)
    date_order = IntField()
    position = ForeignKeyField(Position)
    created = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            # date/bus and date/position must be unique
            (('date', 'bus'), True),
            (('date', 'position'), True),
        )


class User(BaseModel):
    user_id = CharField(primary_key=True)
    full_name = CharField()
    email = CharField(unique=True)
    created = DateTimeField(default=datetime.datetime.now())
    bus = ForeignKeyField(Bus)


class AdminUser(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    created = DateTimeField(default=datetime.datetime.now())


all_tables = [Position, Bus, Assignment, User, AdminUser]
