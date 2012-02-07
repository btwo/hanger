#!/usr/bin/env python2
# coding=utf-8
import json
import utils

from tornado import web
from model import Person
from jinja2 import Environment, FileSystemLoader

class Base(web.RequestHandler):
    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if cookie:
            user_json = json.loads(cookie)
            user = Person.get_by(id=int(user_json['id']))
            if user: return user
        return False

    def render_string(self, template_name, **methods):
        '''Template render by Jinja2.'''
        methods.update(
            {'xsrf': self.xsrf_form_html,
            'request': self.request,
            'settings': self.settings,
            'me': self.current_user,
            'static': self.static_url,
            'handler': self,}
        )
        methods.update(self.ui) # UI methods.
        template = self.get_template(template_name)
        html = template.render(methods)
        return utils.remove_space(html)

    def get_template(self, template_name):
        '''Get jinja2 template object.'''
        env = Environment(
            loader = FileSystemLoader(self.settings['template_path']),
            auto_reload = self.settings['debug'],
            autoescape = False,
        )
        template = env.get_template(template_name)
        return template

    def get_error_html(self, status_code, **kwargs):
        if status_code == 404:
            return self.render_string('errors/404.html')
        self.write(str(status_code) + 'error')

    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def redirect(self, to = None):
        if not to:
            to = self.get_argument("next", None)
            if not to: to = '/'
        super(Base, self).redirect(to)

    def item(self, Item, itemid):
        item = Item.get_by(id = int(itemid))
        if not item:
            raise web.HTTPError(404)
        return item 

    def form_validate(self, form, **kwargs):
        if not form.validate():
            self.render(self.templname, form = form, **kwargs)
            return False
        return True
