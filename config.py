#!/usr/bin/env python2
# coding=utf-8
from os.path import join
from app import ui, PATH

#setting
settings = {}
settings['debug'] = True
settings['ui_methods'] = ui
settings['port'] = 8888
# Path
settings['template_path'] = join(PATH, 'templates')
settings['static_path'] = join(PATH, 'static')
settings['avatar_path'] = join(settings['static_path'], 'avatar')
settings['logfile_path'] = join(PATH, 'error.log')
# url
settings['login_url'] = '/signin/'
# Security
settings['xsrf_cookies'] = True
settings['cookie_secret'] = 'OTL'
