#!/usr/bin/env python2
# coding=utf-8
from os.path import join
from app import PATH, ui

#setting
settings = dict(
    debug = True,
    ui_methods = ui,
    port = 8888,
    login_url = '/signin/',
    # Security
    xsrf_cookies = True,
    cookie_secret = r'HaHaNiKanKanNi!Yooooooooooooooooooooooooooooo~~~'
)
# Path
settings['template_path'] = join(PATH, 'templates')
settings['static_path'] = join(PATH, 'static')
settings['avatar_path'] = join(settings['static_path'], 'avatar')
settings['logfile_path'] = join(PATH, 'error.log')
