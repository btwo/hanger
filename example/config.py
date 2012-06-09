#!/usr/bin/env python2.7
# coding=utf-8
import os.path
import ui_methods
from hanger.utils import random_string, realpath

ownpath = realpath(__file__)
ad = lambda p: os.path.join(ownpath, p) # absolute directory maker.

def secret(config):
    '''Load cookie secret from file, if not such file, whill be create one.'''
    try:
        secret = open(config['cookie_secret_file'])
    except IOError:
        config['cookie_secret'] = random_string(30)
        secret = open(config['cookie_secret_file'], "w")
        secret.write(config['cookie_secret'])
        secret.close()
    else:
        config['cookie_secret'] = secret.readline()
        secret.close()
    return config

config = {
    "site_name": "Hanger", # your website name, support unicode.
    "site_domain": "foo.bar", # site domain, not affect debug.
    "debug": True, # debug mode.
    "port": 8888, # application port.
    "database_url": "sqlite:////tmp/hanger.db",
    "xsrf_cookies": True,
    "cookie_secret_file": ad("conf/secret"),
    "send_error_email": True,
    "admin_mail": "example@foo.bar", # if server occur the error, mail to.
    "mail_host": "127.1", # mail server.
    "logfile": ad("log/application.log"), # application error logfile.
}

app_config = {
    "ui_methods": ui_methods,
    "login_url": "/signin/",
    "template_path": ad("templates"),
    "static_path": ad("static"),
    "media_path": ad("media"),
    "media_url": "/media/",
    "avatar_path": ad("media/avatar"),
    "avatar_url": "/media/avatar/",
}

redis_config = {
    "redis_port": 6379, # this number must to same as `conf/redis.conf`.
    "redis_db": 0, # the number of redis database serial.
    "redis_db_filename": "redis.rdb",
    "redis_logfile": ad("conf/redis.conf"),
}

config = secret(config)
config.update(app_config)
config.update(redis_config)
