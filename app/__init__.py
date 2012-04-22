#!/usr/bin/env python2
# coding=utf-8
from os import path
PATH = path.split(path.realpath(__file__))[0]

from lib.database import SQLAlchemy
db = SQLAlchemy('sqlite:////tmp/hanger.db')

import utils
import view
import model
import forms


from tornado import web
from config import settings
from view import Home, SignIn, SignUp, SignOut, PersonPage, Settings
from base import Base


class Error404(Base):
    '''If url not belonging to any handler, raise 404error.'''
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


routes = [
    # This is url route rule
    (r'/', Home),
    (r'/signin/?', SignIn),
    (r'/signup/?', SignUp),
    (r'/signout/?', SignOut),
    (r'/person/(\d+)/?', PersonPage),
    (r'/settings/?', Settings),
    (r'.*', Error404),
]


class Application(web.Application):
    def __init__(self):
        super(Application, self).__init__(routes, **settings)
