#!/usr/bin/env python2
# coding=utf-8
import os
import logging

from lib import ui
from tornado import options

PATH = os.path.split(os.path.realpath(__file__))[0] 
settings = {}
settings['debug'] = True
settings['ui_methods'] = ui
settings['port'] = 8888
# Path
settings['template_path'] = PATH + '/templ'
settings['static_path'] = PATH + '/static'
settings['log_path'] = PATH + '/app.log'
settings['avatar_path'] = settings['static_path'] + '/avatar/'
# url
settings['login_url'] = '/signin/'
# Security
settings['xsrf_cookies'] = True
settings['cookie_secret'] = 'ThisCookieSecret(=w=)' #TODO random secret.
#TODO: MySQL.

def log_config():
    if settings['debug']:
        options.parse_command_line()
    else:
        logging.basicConfig(
            #set log output.
            filename = settings['log_path'],
            level = logging.WARN,
        ) 
    return
