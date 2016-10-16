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
    last_updated = DateTimeField()


class Bus(BaseModel):
    name = CharField(primary_key=True)


class Assignment(BaseModel):
    date = DateField()
    bus = ForeignKeyField(Bus)
    position = ForeignKeyField(Position)
    arrived = TimeField()

    class Meta:
        indexes = (
            # a bus can have only one position per day
            (('date', 'bus', 'position'), True),
        )


class User(BaseModel):
    user_id = CharField(primary_key=True)
    full_name = CharField()
    email = CharField(unique=True)
    created_at = DateTimeField(default=datetime.datetime.now())
    bus = ForeignKeyField(Bus)


class AdminUser(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    created = DateTimeField(default=datetime.datetime.now())


all_tables = [Position, Bus, Assignment, User, AdminUser]
