#!/usr/bin/env python2
# coding=utf-8
from os.path import join
from example import PATH, ui

settings = dict(
    # general
    debug = True,
    ui_methods = ui,
    port = 8888,
    login_url = '/signin/',
    # Security
    xsrf_cookies = True,
    cookie_secret = r'哈哈哈你看看你',
    # path
    template_path = join(PATH, 'templates'),
    static_path = join(PATH, 'static'),
    logfile_path = join(PATH, 'error.log'),
)
settings['avatar_path'] = join(settings['static_path'], 'avatar')
