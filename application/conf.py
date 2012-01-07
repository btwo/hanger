#!/usr/bin/env python2
# coding=utf-8
import os
# copy to utils, because cannot import
PATH = os.path.split(os.path.realpath(__file__))[0] 
settings = dict(
    #Site and application settings.
    debug = True,
    template_path = PATH + '/templates',
    static_path = PATH + '/static',
    log_path = PATH + '/app.log',
    login_url = '/sign/in/',
    site_url = 'http://127.0.0.1:8888',
    xsrf_cookies = True,
    cookie_secret = r'ThisIsTheCookieSecret_2012/1/7/12:14.',
    hash_salt = '**salt**',
)
