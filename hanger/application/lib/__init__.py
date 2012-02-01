#!/usr/bin/env python2
# coding=utf-8
import view
import model

from tornado import web
from config import settings
from view import Home, SignIn, SignUp, SignOut, PersonPage, Error404, Settings

handlers = [
    (r'/?', Home),
    (r'/signin/?', SignIn),
    (r'/signup/?', SignUp),
    (r'/signout/?', SignOut),
    (r'/person/(\d+)/?', PersonPage),
    (r'/settings/?', Settings),
    (r'.*', Error404), #If url not belonging to any handler, raise 404error.
]

class App(web.Application):
    def __init__(self):
        super(App, self).__init__(handlers, **settings)
