#!/usr/bin/env python2
# coding=utf-8
from lib import utils
PATH = utils.realpath(__file__)

from tornado import web
from config import settings, db, env
from view import Home, SignIn, SignUp, SignOut, PersonPage, Settings
from base import Base

class PageNotFound(Base):
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
    (r'.*', PageNotFound), # Place to end.
]


class Application(web.Application):
    def __init__(self):
        self.env = env
        super(Application, self).__init__(routes, **settings)

application = Application()
