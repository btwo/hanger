#!/usr/bin/env python2
# coding=utf-8
from tornado import web
from lib.hanger import BaseHandler, JinjaMixin, AutomationMixin

class Base(AutomationMixin, JinjaMixin, BaseHandler):
    def get_error_html(self, status_code, **kwargs):
        try:
            return self.render_string('errors/%d.html' % status_code, **kwargs)
        except:
            self.set_header('Content-Type', 'text/plan')
            return "Sorry, an %d HTTP Error has occurred." % status_code


class PageNotFound(Base):
    '''If url not belonging to any handler, raise 404error.'''
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


class Home(Base):
    def get(self):
        self.render()
