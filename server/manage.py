import argparse
import bcrypt
import getpass

from database import db, all_tables, AdminUser, Bus
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
        print('id {}: {}: {}'.format(admin.id,
            admin.username, admin.password))

def bus_add(args):
    name = args.bus_name
    Bus.create(name=name)
    print('Bus {} created.'.format(name))

def bus_list(args):
    for bus in Bus.select():
        print('{}'.format(bus.name))


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


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
