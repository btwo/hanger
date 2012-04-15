#!/usr/bin/env python2
# coding=utf-8
import view
import model

from tornado import web
from base import Base
from view import Home, SignIn, SignUp, SignOut, PersonPage, Settings

class Error404(Base):
    '''If url not belonging to any handler, raise 404error.'''
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


handlers = [
    (r'/', Home),
    (r'/signin/?', SignIn),
    (r'/signup/?', SignUp),
    (r'/signout/?', SignOut),
    (r'/person/(\d+)/?', PersonPage),
    (r'/settings/?', Settings),
    (r'.*', Error404),
]

class App(web.Application):
    def __init__(self, settings):
        super(App, self).__init__(handlers, **settings)
