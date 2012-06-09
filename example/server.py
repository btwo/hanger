#!/usr/bin/env python2.7
# coding=utf-8
# recommand run `python2.7 -R` fix the Hash Collision DoS
from application import application
from tornado import httpserver, ioloop, options
from config import config

def run():
    '''start logging, load application and start the server.'''
    # first should create database: ./dbinit.py
    if not config['debug']:
        options.options.log_file_prefix = config['logfile']
    options.parse_command_line()
    http_server = httpserver.HTTPServer(application)
    http_server.listen(config['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.


if __name__ == '__main__':
    run()
