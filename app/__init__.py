#!/usr/bin/env python2
# coding=utf-8
import view
import model
import forms
import utils


from tornado import web
from view import Home, SignIn, SignUp, SignOut, PersonPage, Settings
from base import Error404



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
