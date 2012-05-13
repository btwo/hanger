#!/usr/bin/env python2
# coding=utf-8
from lib import utils
PATH = utils.realpath(__file__)
from tornado import web
from config import settings
from lib.database import SQLAlchemy

db = SQLAlchemy('sqlite:////tmp/hanger.db') # first run, run db.create_all().

from view import Home, SignIn, SignUp, SignOut, PersonPage, Settings,\
        PageNotFound
routes = [
    # This is url route rule
    (r'/', Home),
    (r'/signin/?', SignIn),
    (r'/signup/?', SignUp),
    (r'/signout/?', SignOut),
    (r'/person/(\d+)/?', PersonPage),
    (r'/settings/?', Settings),
    (r'.*', PageNotFound), # Place to end.
]


class Application(web.Application):
    def __init__(self):
        super(Application, self).__init__(routes, **settings)

application = Application()
