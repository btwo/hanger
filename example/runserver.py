#!/usr/bin/env python2.7
# coding=utf-8
import json
import re

from example import Application
from tornado import httpserver, ioloop, options

def run(config):
    # first should create database: ./dbinit.py
    if not config['debug']:
        options.options.log_file_prefix = config['logfile_path']
    options.parse_command_line()
    application = Application(config)
    http_server = httpserver.HTTPServer(application)
    http_server.listen(config['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.

def get_config():
    config_file = open("conf/config.json")
    string = config_file.read()
    config = json.loads(unicode(string.decode("utf-8")))
    config_file.close()
    return config

if __name__ == '__main__':
    run(get_config())
