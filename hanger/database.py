#!/usr/bin/env python2
# coding=utf-8
'''
Elixir.
'''
import datetime
import elixir

from sqlalchemy import types
from elixir import Field

class Elixir(object):
    def __init__(self, master, **kwargs):
        self.metadata = elixir.metadata
        self.metadata.bind = master
        self.metadata.bind.echo = False
        self.session = elixir.session
        elixir.setup_all()

    def create_db(self):
        elixir.create_all()


class Entity(elixir.Entity):
    created = Field(types.DateTime())

    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.created = datetime.datetime.now()
