#!/usr/bin/env python2
# coding=utf-8
import os
import elixir
import lib

from config import settings, log_config
from tornado import httpserver, ioloop

def run():
    database()
    log_config()
    server()

def database():
    db_filename = 'sqlite'
    elixir.metadata.bind = 'sqlite:///' + db_filename #Path.
    elixir.setup_all()
    if not os.path.exists(db_filename):
        elixir.metadata.bind.echo = True
        elixir.create_all()
    elixir.metadata.bind.echo = False

def server():
    http_server = httpserver.HTTPServer(lib.App())
    http_server.listen(settings['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.

if __name__ == '__main__':
    run()
