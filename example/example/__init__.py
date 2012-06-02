#!/usr/bin/env python2
# coding=utf-8
from os.path import join
from hanger import utils
from tornado import web
from hanger.database import Elixir
import model

db = Elixir('sqlite:////tmp/hanger.db') # first run, run db.create_all().

import user
import views


class Application(web.Application):
    def __init__(self, config):
        # Settings extend.
        import ui
        #url roues
        routes = []
        routes.extend(user.routes)
        routes.extend(views.routes)
        routes.append(('.*', views.PageNotFound)) # 404 page, place bottom.
        super(Application, self).__init__(
            routes, ui_methods=ui, **config_handler(config))


def config_handler(config):
    PATH = utils.realpath(__file__)
    keys = ['template_path', "static_path", "logfile_path"]
    for key in keys:
        config[key] = join(PATH, config[key])

    config['avatar_path'] = join(config['static_path'], 'avatar')
    return config
