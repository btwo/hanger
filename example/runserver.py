#!/usr/bin/env python2.7
# coding=utf-8
import json

from {{{app_name}}} import Application
from tornado import httpserver, ioloop, options
from utils import get_config

def run(config):
    # first should create database: ./dbinit.py
    if not config['debug']:
        options.options.log_file_prefix = config['logfile_path']
    options.parse_command_line()
    application = Application(config)
    http_server = httpserver.HTTPServer(application)
    http_server.listen(config['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.


if __name__ == '__main__':
    run(get_config())
