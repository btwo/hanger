#!/usr/bin/env python2
# coding=utf-8
from tornado import web
from hanger.database import Elixir
from redis import StrictRedis
from config import config, ad
import model

db = Elixir(config['database_url']) # first run, run db.create_all().

import user
import views

class Application(web.Application):
    def __init__(self):
        self.redis = StrictRedis(host='localhost', port=config['redis_port'],
            db=config['redis_db'])
        # Settings extend.
        #url roues
        routes = []
        modules = [user, views]
        for view in modules:
            routes.extend(view.routes)
        routes.extend([
            (r"/media/(.*)", web.StaticFileHandler, {"path": ad("media")}),
            ('.*', views.PageNotFound)], # 404 page, place bottom.
        )

        super(Application, self).__init__(routes, **config)

application = Application()
