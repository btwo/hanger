#!/usr/bin/env python2
# coding=utf-8

from app import application
from config import settings
from tornado import httpserver, ioloop, options

# first should create database: model.create_all()
if not settings['debug']:
    options.options.log_file_prefix = settings['logfile_path']
options.parse_command_line()
http_server = httpserver.HTTPServer(application)
http_server.listen(settings['port'])
ioloop.IOLoop.instance().start() #Start IO Loop.
