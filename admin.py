#!/usr/bin/env python2
# coding=utf-8
import os
import readline
import elixir

from application import orm

def main():
    print('1. init')
    print('2. New user.')
    user_input = raw_input()
    if user_input == '1': init()
    elif user_input == '2': new_user()

def init():
    if os.path.exists('database'):
        os.remove('database') #remove sqlite datebase
    orm.metadata.bind.echo = True
    elixir.setup_all(True)
    new_user()
    print('all done.')

def new_user():
    print('New user')
    name = raw_input('Name:\n').decode("utf8")
    email = raw_input('Email:\n')
    password = raw_input('Password:\n')
    orm.Person(name, email, password)
    elixir.session.commit()

if __name__ == '__main__': main()
