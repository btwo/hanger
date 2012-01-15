#!/usr/bin/env python2
# coding=utf-8
import datetime

from utils import escape, string_hash, url_escape
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
        self.name = escape(name)
        self.email = escape(email)
        self.password = string_hash(password)
        self.created = datetime.datetime.now()

metadata.bind = 'sqlite:///database'
metadata.bind.echo = False
