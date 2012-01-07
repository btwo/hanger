#!/usr/bin/env python2
# coding=utf-8
import os
import logging

from tornado import web, httpserver, ioloop
from application import orm
from application.urls import handlers

settings = dict(
    #Site and application settings.
    debug = True,
    template_path = './application/templates',
    static_path = './application/static',
    login_url = '/sign/in/',
    site_url = 'http://127.0.0.1:8888',
    xsrf_cookies = True,
    cookie_secret = r'ThisIsTheCookieSecret_2012/1/6/19:23.',
)


app = web.Application(handlers, **settings)

def server_run(port):
    orm.setup_all() #ORM setup.
    http_server = httpserver.HTTPServer(app) #Server
    http_server.listen(port)
    logging.basicConfig(
        filename = os.path.join(os.getcwd(), './log/app.log'),
        level = logging.DEBUG) #set log output.
    ioloop.IOLoop.instance().start() #Start IO Loop

if __name__ == '__main__':
    server_run(8888)
