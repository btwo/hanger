#!/usr/bin/env python2
# coding=utf-8
from os.path import join
from tornado import web
from hanger.database import Elixir
from redis import StrictRedis
import model

db = Elixir('sqlite:////tmp/hanger.db') # first run, run db.create_all().

import user
import views


class Application(web.Application):
    def __init__(self, config):
        import ui
        config = config_handler(config)
        self.redis = StrictRedis(
            host='localhost', port=config['redis_port'], db=config['redis_db'])
        # Settings extend.
        #url roues
        routes = []
        routes.extend(user.routes)
        routes.extend(views.routes)
        routes.append(('.*', views.PageNotFound)) # 404 page, place bottom.
        super(Application, self).__init__(
            routes, ui_methods=ui, **config)


def config_handler(config):
    config['avatar_path'] = join(config['static_path'], 'avatar')
    return config
