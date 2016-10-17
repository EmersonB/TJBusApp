import argparse
import bcrypt
import datetime
import getpass
from playhouse.shortcuts import model_to_dict

from database import db, all_tables, AdminUser, Bus, Position
from utils import pwhash

def db_create_tables(args):
    db.connect()
    db.create_tables(all_tables)
    print('Tables created.')

def admin_add(args):
    username = args.username
    password = pwhash.hash(getpass.getpass())
    AdminUser.create(username=username, password=password)
    print('Admin {} created.'.format(username))

def admin_list(args):
    for admin in AdminUser.select():
        print('id {id}: {username} / {password}'.format(**model_to_dict(admin)))

def bus_add(args):
    bus = Bus.create(name=args.bus_name)
    print('Bus created with name {}'.format(bus.name))

def bus_list(args):
    for bus in Bus.select():
        print('name: {name}'.format(**model_to_dict(bus)))

def position_add(args):
    position = Position.create(map_x=args.map_x, map_y=args.map_y, angle=args.angle)
    print('Position created with id {}'.format(position.id))

def position_list(args):
    for position in Position.select():
        print('id {id}: map_x {map_x}, map_y {map_y}, angle {angle}'.format(**model_to_dict(position)))


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')
subparsers.required = True

# begin db commands
db_parser = subparsers.add_parser('db', help='database setup')
db_subparsers = db_parser.add_subparsers(dest='subcommand')
db_subparsers.required = True

db_parser_create_tables = db_subparsers.add_parser('create-tables', help='create database tables')
db_parser_create_tables.set_defaults(func=db_create_tables)

# begin admin commands
admin_parser = subparsers.add_parser('admin', help='manage admin users')
admin_subparsers = admin_parser.add_subparsers(dest='subcommand')
admin_subparsers.required = True

admin_parser_add = admin_subparsers.add_parser('add', help='add an admin')
admin_parser_add.add_argument('username')
admin_parser_add.set_defaults(func=admin_add)

admin_parser_list = admin_subparsers.add_parser('list', help='list all admins')
admin_parser_list.set_defaults(func=admin_list)

# begin bus commands
bus_parser = subparsers.add_parser('bus', help='manage buses')
bus_subparsers = bus_parser.add_subparsers(dest='subcommand')
bus_subparsers.required = True

bus_parser_add = bus_subparsers.add_parser('add', help='add a bus')
bus_parser_add.add_argument('bus_name')
bus_parser_add.set_defaults(func=bus_add)

bus_parser_list = bus_subparsers.add_parser('list', help='list all buses')
bus_parser_list.set_defaults(func=bus_list)

# begin position commands
position_parser = subparsers.add_parser('position', help='manage positions')
position_subparsers = position_parser.add_subparsers(dest='subcommand')
position_subparsers.required = True

position_subparser_add = position_subparsers.add_parser('add', help='add a position')
position_subparser_add.add_argument('map_x', type=float)
position_subparser_add.add_argument('map_y', type=float)
position_subparser_add.add_argument('angle', type=float)
position_subparser_add.set_defaults(func=position_add)

position_subparser_list = position_subparsers.add_parser('list', help='list all positions')
position_subparser_list.set_defaults(func=position_list)


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
