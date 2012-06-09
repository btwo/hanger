#!/usr/bin/env python2.7
# coding=utf-8
from hanger import Hanger
from hanger.database import Elixir
from redis import StrictRedis
from config import config
import model

db = Elixir(config['database_url']) # first run, run db.create_all().

import user
import views

class Application(Hanger):
    def __init__(self):
        self.redis = StrictRedis(host='localhost', port=config['redis_port'],
            db=config['redis_db'])
        #url roues
        end_handlers = [
            ('.*', views.PageNotFound), # 404 page, place bottom.
        ]
        routes = self.route(user, views, end_handlers=end_handlers)
        super(Application, self).__init__(routes, **config)

application = Application()
