#!/usr/bin/env python2
# coding=utf-8
import os
import logging

from tornado import web, httpserver, ioloop
from application import orm
from application.urls import handlers
from application.conf import settings

app = web.Application(handlers, **settings)

def server_run(port):
    orm.setup_all() #ORM setup.
    http_server = httpserver.HTTPServer(app) #Server
    http_server.listen(port)
    logging.basicConfig(
        filename = settings['log_path'],
        level = logging.DEBUG) #set log output.
    ioloop.IOLoop.instance().start() #Start IO Loop

if __name__ == '__main__':
    server_run(8888)
