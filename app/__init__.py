#!/usr/bin/env python2
# coding=utf-8
from lib import utils
PATH = utils.realpath(__file__)
from tornado import web
from config import settings
from lib.database import SQLAlchemy
from jinja2 import Environment, FileSystemLoader

db = SQLAlchemy('sqlite:////tmp/hanger.db') # first run, run db.create_all().

jinja_env = Environment(
    # load template in file system.
    loader = FileSystemLoader(settings['template_path']),
    auto_reload = settings['debug'], #auto reload
    autoescape = False, # auto escape
)

from view import Home, PageNotFound
routes = [
    # This is url route rule
    (r'/', Home),
    (r'.*', PageNotFound), # Place to end.
]


class Application(web.Application):
    def __init__(self):
        super(Application, self).__init__(
            routes, jinja_env=jinja_env, **settings)

application = Application()
