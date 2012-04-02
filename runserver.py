#!/usr/bin/env python2
# coding=utf-8
import os
import elixir
import app

from config import settings
from tornado import httpserver, ioloop, options

def runserver():
    http_server = httpserver.HTTPServer(app.App())
    http_server.listen(settings['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.

def log():
    if settings['debug']:
        options.options.log_file_prefix = settings['logfile_path']
    options.parse_command_line()
    
def orminit():
    db_filename = 'sqlite'
    elixir.metadata.bind = 'sqlite:///' + db_filename #Path.
    elixir.setup_all()
    if not os.path.exists(db_filename):
        elixir.metadata.bind.echo = True
        elixir.create_all()
    elixir.metadata.bind.echo = False

if __name__ == '__main__':
    orminit()
    log()
    runserver()
