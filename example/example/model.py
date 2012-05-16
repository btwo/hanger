#!/usr/bin/env python2
# coding=utf-8
import datetime

from utils import escape, password_hash
from sqlalchemy import Column, Integer, String, DateTime
from example import db

session = db.session

class Base(object):
    id = Column(Integer, primary_key=True)
    created = Column(DateTime)

    def __init__(self):
        self.created = datetime.datetime.now()


class Person(Base, db.Model):
    __tablename__ = 'users'

    name = Column(String)
    email = Column(String)
    password = Column(String)
    avatar = Column(String)
    bio = Column(String)

    def __init__(self, name, email, password):
        super(Person, self).__init__()
        self.name = escape(name)
        self.email = escape(email)
        self.password = password_hash(password, email=self.email)

    def __repr__(self):
        return "<Person ('%s', '%s')>" % (self.id, self.name)

    def hash_password(self, password):
        return password(password, email=self.email)

    def change_password(self, password):
        self.password = self.hash_password(password)

    def change_name(self, name):
        self.name = escape(name)

    def change_bio(self, bio):
        self.bio = escape(bio)


def getuser(**kwargs):
    return Person.query.filter_by(**kwargs).first()
