#!/usr/bin/env python2.7
# coding=utf-8
import json

from hanger import BaseHandler, JinjaMixin, AutoFormsMixin,\
        AutoTemplatesMixin, MailMixin
from model import getuser

class Base(MailMixin, AutoFormsMixin, AutoTemplatesMixin, JinjaMixin,
           BaseHandler):
    '''The base handler of user request.'''

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.redis = self.application.redis

    def get_error_html(self, status_code, **kwargs):
        if not self.settings['debug'] and status_code is 500:
            # send mail to admin when 500 error is occur.
            self.send_error_mail('mail/500error', **kwargs) 
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
