#!/usr/bin/env python2
# coding=utf-8
import logging

from tornado import web, options, httpserver, ioloop
from application import orm
from application.urls import handlers
from application.conf import settings

app = web.Application(handlers, **settings)

def log_config():
    if settings['debug']:
        options.parse_command_line()
        return
    logging.basicConfig(filename = settings['log_path'],
        level = logging.WARN) #set log output.

def server_run(port):
    log_config()
    orm.setup_all() #ORM setup.
    http_server = httpserver.HTTPServer(app) #Server
    http_server.listen(port)
    ioloop.IOLoop.instance().start() #Start IO Loop

if __name__ == '__main__':
    server_run(settings['port'])
