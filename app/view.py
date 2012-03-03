#!/usr/bin/env python2
# coding=utf-8
import os
import json
import StringIO
import Image

from base import Base
from model import getitem
from elixir import session
from tornado import web

class Home(Base):
    def get(self):
        self.render()
