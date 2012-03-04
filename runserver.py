#!/usr/bin/env python2
# coding=utf-8
import os
import elixir
import app

from config import settings, logging_config
from tornado import httpserver, ioloop

def runserver():
    database()
    logging_config()
    http_server = httpserver.HTTPServer(app.App())
    http_server.listen(settings['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.

def database():
    db_filename = 'sqlite'
    elixir.metadata.bind = 'sqlite:///' + db_filename #Path.
    elixir.setup_all()
    if not os.path.exists(db_filename):
        elixir.metadata.bind.echo = True
        elixir.create_all()
    elixir.metadata.bind.echo = False

if __name__ == '__main__':
    runserver()
