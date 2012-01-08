#!/usr/bin/env python2
# coding=utf-8
import sys
import os
import readline
import elixir
import getpass

from application import orm

def router():
    orm.metadata.bind.echo = True
    elixir.setup_all(True)
    option = sys.argv[1:]
    if (not option) or option[0] == 'help': admin_help()
    elif option[0] == 'init': init()
    elif option[0] == 'user':
        if option[1] == 'new': new_user()

def init():
    if os.path.exists('database'):
        os.remove('database') #remove sqlite datebase
    if raw_input('Are you create new user?') == 'y':
        new_user()

def new_user():
    print('New user')
    name = raw_input('Name:\n').decode("utf8")
    email = raw_input('Email:\n')
    password = getpass.getpass('Password:\n')
    orm.Person(name, email, password)
    orm.session.commit()

def admin_help():
    print('init              : Initialize the database')
    print('user              : User Management')
    print('user new          : Create_user')


if __name__ == '__main__': router()
