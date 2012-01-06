#!/usr/bin/env python2
# coding=utf-8
import datetime
import uuid
import lib
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
    salt = Field(String())
    created = Field(DateTime())

    def __init__(self, name, email, password):
        self.name = lib.escape(name)
        self.email = lib.escape(email)
        self.salt = lib.random_string(10)
        self.password = lib.string_hash(password, self.salt)
        self.created = datetime.datetime.now()

metadata.bind = 'sqlite:///database'
metadata.bind.echo = False
