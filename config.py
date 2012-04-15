#!/usr/bin/env python2
# coding=utf-8
import os

from os.path import join
from app import ui

path = os.path.split(os.path.realpath(__file__))[0] 
settings = {}
settings['debug'] = True
settings['ui_methods'] = ui
settings['port'] = 8888
# Path
settings['template_path'] = join(path, 'templates')
settings['static_path'] = join(path, 'static')
settings['logfile_path'] = join(path, 'error.log')
# url
settings['login_url'] = '/signin/'
# Security
settings['xsrf_cookies'] = True
settings['cookie_secret'] = 'Orz'
