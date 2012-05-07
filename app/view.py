#!/usr/bin/env python2
# coding=utf-8
from tornado import web
from lib.hanger import BaseHandler, JinjaMixin, AutomationMixin

class Base(AutomationMixin, JinjaMixin, BaseHandler):
    def get_error_html(self, status_code, **kwargs):
        code = str(status_code)
        try:
            return self.render_string('errors/'+code+'.html', **kwargs)
        except:
            return self.render_string('errors/unkown.html/', **kwargs)


class PageNotFound(Base):
    '''If url not belonging to any handler, raise 404error.'''
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


class Home(Base):
    def get(self):
        self.render()
