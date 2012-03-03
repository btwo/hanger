#!/usr/bin/env python2
# coding=utf-8
import datetime

from tornado import web
from utils import escape, string_hash
from elixir import Entity, Field
from elixir import UnicodeText, Unicode, String, DateTime
from elixir.relationships import OneToMany, ManyToOne, ManyToMany

def getitem(Item, itemid ,show_error = True):
    item = Item.get_by(id = int(itemid))
    if show_error and not item:
        raise web.HTTPError(404) 
    return item
