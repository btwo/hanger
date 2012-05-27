#!/usr/bin/env python2
# coding=utf-8
from hanger import utils
PATH = utils.realpath(__file__)
from tornado import web
from config import settings
from hanger.database import Elixir
import model

db = Elixir('sqlite:////tmp/hanger.db') # first run, run db.create_all().

import user
import views


class Application(web.Application):
    def __init__(self):
        # Settings extend.
        import ui
        settings['ui_methods'] = ui
        #url roues
        routes = []
        routes.extend(user.routes)
        routes.extend(views.routes)
        routes.append(('.*', views.PageNotFound)) # 404 page, place bottom.
        super(Application, self).__init__(routes, **settings)

application = Application()
