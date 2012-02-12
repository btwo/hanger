#!/usr/bin/env python2
# coding=utf-8
import datetime

from utils import escape, string_hash
from elixir import Entity, Field
from elixir import UnicodeText, Unicode, String, DateTime
from elixir.relationships import OneToMany, ManyToOne, ManyToMany

class Person(Entity):
    name = Field(Unicode())
    email = Field(String())
    password = Field(String())
    avatar = Field(String()) #user avatar file name.
    created = Field(DateTime())
    bio = Field(UnicodeText())

    def __init__(self, name, email, password):
        self.name = escape(name)
        self.email = escape(email)
        self.password = string_hash(password, salt = self.email)
        self.created = datetime.datetime.now()
