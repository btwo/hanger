#!/usr/bin/env python2
# coding=utf-8
from jinja2 import Environment, FileSystemLoader
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
    cookie_secret = r'=w=Kira+10086*66535/23333DAZE'
)
# Path
settings['template_path'] = join(PATH, 'templates')
settings['static_path'] = join(PATH, 'static')
settings['avatar_path'] = join(settings['static_path'], 'avatar')
settings['logfile_path'] = join(PATH, 'error.log')
settings['jinja2_env'] = Environment(
    # load template in file system.
    loader = FileSystemLoader(settings['template_path']),
    auto_reload = settings['debug'], #auto reload
    autoescape = False, # auto escape
    )
