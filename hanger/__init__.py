#!/usr/bin/env python2.7
# coding=utf-8
import json

from tornado import web
from urlparse import urljoin
from template import JinjaMixin, AutoTemplatesMixin
from forms import AutoFormsMixin
from mail import MailMixin
import database
import utils
import forms

class Hanger(web.Application):
    '''Hanger application class.'''
    def __init__(self, handlers=None, *args, **settings):
        if settings.has_key("media_path"):
            self.media_route()
        super(Hanger, self).__init__(handlers, *args, **settings)

    def route(self, *modules, **addhandlers):
        routes = []
        if addhandlers.has_key("top"):
            routes.extend(addhandlers['top'])
        for module in modules:
            if hasattr(module, "routes"):
                routes.extend(module.routes)
        if addhandlers.has_key("end_handlers"):
            routes.extend(addhandlers['end_handlers'])
        return routes

    def media_route(self, handlers, settings):
        '''Add media handler.'''
        media_handler = (
            r"%s(.*)" % settings['media_url'],
            web.StaticFileHandler, {"path": settings['media_path']})
        if settings.has_key("media_path"):
            handlers.insert(0, media_handler)


class BaseHandler(web.RequestHandler):
    '''
    Base handler is parent class of all handlers.
    had some tools for simpliy and enhancement base tornado web framework.
    '''
    def __init__(self, *args, **kwargs):
        self.handler_name = self.__class__.__name__
        super(BaseHandler, self).__init__(*args, **kwargs)

    def media_url(self, url):
        return urljoin(self.settings['media_url'], url)

    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def redirect(self, url):
        url = self.get_argument("next", default = url)
        super(BaseHandler, self).redirect(url)


__all__ = ['utils', 'database', 'forms', 'MailMixin', 'AutoFormsMixin',
           'AutoTemplatesMixin', 'BaseHandler', 'JinjaMixin']
