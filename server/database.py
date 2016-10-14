from peewee import *
db = SqliteDatabase('dev.db')


def create_tables():
    database.connect()
    database.create_tables([User, Relationship, Message])


class BaseModel(Model):
    class Meta:
        database = db


class Position(BaseModel):
    map_x = DoubleField()
    map_y = DoubleField()
    angle = DoubleField()
    last_updated = DateTimeField()


class Bus(BaseModel):
    name = CharField(unique=True)


class Assignment(BaseModel):
    date = DateField()
    bus = ForeignKeyField(Bus)
    position = ForeignKeyField(Position)
    last_updated = DateTimeField()

