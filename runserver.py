#!/usr/bin/env python2
# coding=utf-8
import os
import app

from app import model
from config import settings
from tornado import httpserver, ioloop, options

def runserver():
    model.create_all()
    if not settings['debug']:
        options.options.log_file_prefix = settings['logfile_path']
    options.parse_command_line()
    http_server = httpserver.HTTPServer(app.App())
    http_server.listen(settings['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.


if __name__ == '__main__':
    runserver()
