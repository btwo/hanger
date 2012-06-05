#!/usr/bin/env python2.7
# coding=utf-8
import example
from os.path import join
from example import Application
from tornado import httpserver, ioloop, options
from hanger.utils import realpath

j = lambda p: join(realpath(example.__file__), p)

config = {
    "site_name": "Hanger",
    "site_domain": "127.0.0.1",
    "debug": True,
    "port": 8888,
    "redis_port": 6379,
    "redis_db": 0,
    "login_url": "/signin/",
    "xsrf_cookies": True,
    "cookie_secret": "{{{random_secret}}}",
    "send_error_email": True,
    "admin_mail": "tioover@gmail.com",
    "mail_host": "127.1",
    "template_path": j("templates"),
    "static_path": j("static"),
}

def run():
    # first should create database: ./dbinit.py
    options.parse_command_line()
    application = Application(config)
    http_server = httpserver.HTTPServer(application)
    http_server.listen(config['port'])
    ioloop.IOLoop.instance().start() #Start IO Loop.


if __name__ == '__main__':
    run()
