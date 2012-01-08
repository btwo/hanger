#!/usr/bin/env python2
# coding=utf-8
import os
import readline
import elixir
import getpass

from application import orm

def init():
    if os.path.exists('database'):
        os.remove('database') #remove sqlite datebase
    orm.metadata.bind.echo = True
    elixir.setup_all(True)
    raw_input('Are you create new user?')
    new_user()

def new_user():
    print('New user')
    name = raw_input('Name:\n').decode("utf8")
    email = raw_input('Email:\n')
    password = getpass.getpass('Password:\n')
    orm.Person(name, email, password)
    orm.session.commit()


if __name__ == '__main__': init()
