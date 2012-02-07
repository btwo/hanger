#!/usr/bin/env python2
# coding=utf-8
import os
import logging
import elixir
import lib

from config import settings
from tornado import options, httpserver, ioloop

def run():
    database()
    server()

def database():
    db_filename = 'sqlite'
    elixir.metadata.bind = 'sqlite:///' + db_filename
    elixir.setup_all()
    if not os.path.exists(db_filename):
        elixir.metadata.bind.echo = True
        elixir.create_all()
    elixir.metadata.bind.echo = False

def log_config():
    if settings['debug']:
        options.parse_command_line()
        return
    logging.basicConfig(
        #set log output.
        filename = settings['log_path'],
        level = logging.WARN,
    ) 

def server():
    http_server = httpserver.HTTPServer(lib.App())
    http_server.listen(settings['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.

if __name__ == '__main__':
    run()
