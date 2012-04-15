#!/usr/bin/env python2
# coding=utf-8
import os

from os.path import join
from app import ui

# paths
path = os.path.split(os.path.realpath(__file__))[0] 
appdir = join(path, 'app')

#setting
settings = {}
settings['debug'] = True
settings['ui_methods'] = ui
settings['port'] = 8888
# Path
settings['template_path'] = join(appdir, 'templates')
settings['static_path'] = join(appdir, 'static')
settings['avatar_path'] = join(settings['static_path'], 'avatar')
settings['logfile_path'] = join(path, 'error.log')
# url
settings['login_url'] = '/signin/'
# Security
settings['xsrf_cookies'] = True
settings['cookie_secret'] = 'OTL'
