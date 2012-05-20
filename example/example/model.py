#!/usr/bin/env python2
# coding=utf-8
from utils import escape, string_hash
from elixir import session, Field
from sqlalchemy import types
from hanger.database import Entity

class Person(Entity):
    name = Field(types.Unicode(32))
    email = Field(types.String(256))
    password = Field(types.String(256))
    avatar = Field(types.String(32))
    bio = Field(types.Unicode())

    def __init__(self, name, email, password):
        super(Person, self).__init__()
        self.name = escape(name)
        self.email = escape(email)
        self.password = self.hash_password(password)

    def __repr__(self):
        return "<Person #%s [%s]>" % (self.id, self.name)

    def hash_password(self, password):
        return string_hash(password, salt=self.email)


def getuser(**kwargs):
    return Person.query.filter_by(**kwargs).first()
