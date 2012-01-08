#!/usr/bin/env python2
# coding=utf-8
import datetime
import utils
#Elixir ORM
#Base
from elixir import Entity, Field, metadata
#DataType
from elixir import UnicodeText, Unicode, String, DateTime, Boolean, Integer
#relationships
from elixir import OneToMany, ManyToOne, ManyToMany
#action
from elixir import session, setup_all

class Person(Entity):
    name = Field(Unicode())
    email = Field(String())
    password = Field(String())
    avatar = Field(String()) #user avatar file name.
    created = Field(DateTime())

    def __init__(self, name, email, password):
        self.name = utils.escape(name)
        self.email = utils.escape(email)
        self.password = utils.string_hash(password)
        self.created = datetime.datetime.now()

metadata.bind = 'sqlite:///database'
metadata.bind.echo = False
