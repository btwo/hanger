#!/usr/bin/env python2
# coding=utf-8
import os
import uifunc
PATH = os.path.split(os.path.realpath(__file__))[0] 
settings = dict(
    #Site and application settings.
    debug = True,
    template_path = PATH + '/templates',
    static_path = PATH + '/static',
    log_path = PATH + '/app.log',
    login_url = '/signin/',
    site_url = 'http://127.0.0.1:8888',
    xsrf_cookies = True,
    cookie_secret = r'ThisIsTheCookieSecret_2012/1/11/23:36.',
    hash_salt = '**salt**',
    ui_methods = uifunc,
    port = 8888,
)
