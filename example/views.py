#!/usr/bin/env python2.7
# coding=utf-8
from tornado import web
from base import Base

class PageNotFound(Base):
    '''If url not belonging to any handler, raise 404error.'''
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


class Home(Base):
    def get(self):
        self.render()


routes = [
    (r'/', Home),
]
