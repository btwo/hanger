#!/usr/bin/env python2.7
# coding=utf-8
from utils import escape, string_hash
from sqlalchemy import Column, types
from application import db

class Person(db.Model):
    name = Column(types.Unicode(32), unique=True)
    email = Column(types.String(256), unique=True)
    password = Column(types.String(256))
    avatar = Column(types.String(32))
    bio = Column(types.Unicode())

    def __init__(self, name, email, password):
        super(Person, self).__init__()
        self.name = escape(name)
        self.email = escape(email)
        self.password = self.hash_password(password)

    def __repr__(self):
        return "<Person #%d [%s]>" % (self.id, self.name)

    def hash_password(self, password):
        return string_hash(password, salt=self.email)


def getuser(**kwargs):
    return Person.query.filter_by(**kwargs).first()
