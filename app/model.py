#!/usr/bin/env python2
# coding=utf-8
import datetime

from utils import escape, string_hash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////tmp/hanger.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Person(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    avatar = Column(String)
    bio = Column(String)
    created = Column(DateTime)

    def __init__(self, name, email, password):
        self.name = escape(name)
        self.email = escape(email)
        self.password = string_hash(password, salt = self.email)
        self.created = datetime.datetime.now()

    def __repr__(self):
        return "<Person ('%s', '%s')>" % (self.id, self.name)

    def hash_password(self, password):
        return string_hash(password, salt = self.email)

    def change_password(self, password):
        self.password = self.hash_password(password)

    def change_name(self, name):
        self.name = escape(name)

    def change_bio(self, bio):
        self.bio = escape(bio)


def getuser(uid = None, email = None, name = None):
    query = session.query(Person)
    if uid:
        return query.filter_by(id = int(uid)).first()
    elif email:
        return query.filter_by(email = email).first()
    elif name:
        return query.filter_by(name = name).first()
    return None

def create_all():
    Base.metadata.create_all(engine)
