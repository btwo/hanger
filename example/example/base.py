#!/usr/bin/env python2
# coding=utf-8
import json

from hanger import BaseHandler, JinjaMixin, AutoFormsMixin, AutoTemplatesMixin
from model import getuser

class Base(AutoFormsMixin, AutoTemplatesMixin, JinjaMixin, BaseHandler):
    def get_error_html(self, status_code, **kwargs):
        super(Base, self).get_error_html(status_code, **kwargs)
        try:
            return self.render_string('errors/%d.html' % status_code, **kwargs)
        except:
            self.set_header('Content-Type', 'text/plan')
            return "Sorry, an %d HTTP Error has occurred." % status_code

    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if not cookie:
            return None
        user_id = int(json.loads(cookie)['id'])
        user = getuser(id=user_id)
        if user:
            return user
