#!/usr/bin/env python2
# coding=utf-8
import datetime

from tornado import web
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

    def hash_password(self, password):
        return string_hash(password, salt = self.email)

    def change_password(self, password):
        self.password = self.hash_password(password)

    def change_name(self, name):
        self.name = escape(name)

def getitem(Item, itemid):
    item = Item.get_by(id = int(itemid))
    if not item:
        raise web.HTTPError(404) 
    return item
