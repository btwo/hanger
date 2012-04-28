#!/usr/bin/env python2 
# coding=utf-8 
import json
import lib.base

from model import getuser

class Base(lib.base.Base):
    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if not cookie: return False
        user_json = json.loads(cookie)
        user = getuser(user_json['id'])
        if user: return user
