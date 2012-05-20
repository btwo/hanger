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
    def __init__(self, database, echo=False, **kwargs):
        self.metadata = elixir.metadata
        self.metadata.bind = database
        self.metadata.bind.echo = echo
        elixir.setup_all()

    def create_db(self):
        elixir.create_all()


class Entity(elixir.entity.EntityBase):
    __metaclass__ = elixir.entity.EntityMeta
    created = Field(types.DateTime())

    def __init__(self, *args, **kwargs):
        super(Entity, self).__init__(*args, **kwargs)
        self.created = datetime.datetime.now()
