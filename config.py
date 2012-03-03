#!/usr/bin/env python2
# coding=utf-8
import os
import logging

from os.path import join
from app import ui
from tornado import options

path = os.path.split(os.path.realpath(__file__))[0] 
settings = {}
settings['debug'] = True
settings['ui_methods'] = ui
settings['port'] = 8888
# Path
settings['template_path'] = join(path, 'templ')
settings['static_path'] = join(path, 'static')
settings['log_path'] = join(path, 'error.log')
# url
settings['login_url'] = '/signin/'
# Security
settings['xsrf_cookies'] = True
settings['cookie_secret'] = 'Orz'

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
