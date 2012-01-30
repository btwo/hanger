#!/usr/bin/env python2
# coding=utf-8
import os
import getpass
import readline

from application.conf import settings
from application import orm

def init():
    if os.path.exists('database'):
        os.remove('database') #remove sqlite datebase
    orm.metadata.bind.echo = True
    orm.setup_all(True)
    os.mkdir(settings['avatar_path'])
    print('---------'
          'All done, please edit application/conf.py'
          'settings["cookie_secret"], and settings["hash_salt"]')

def new_user():
    print('New user')
    name = raw_input('Name:\n').decode("utf8")
    email = raw_input('Email:\n')
    password = getpass.getpass('Password:\n')
    orm.Person(name, email, password)
    orm.session.commit()


if __name__ == '__main__':
    init()
