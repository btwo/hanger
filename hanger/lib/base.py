#!/usr/bin/env python2 
# coding=utf-8 
import json
import utils

from tornado import web
from model import Person
from jinja2 import Environment, FileSystemLoader

class Base(web.RequestHandler):
    '''Base Handler'''
    templname = ''
    forms = {}

    def __init__(self, *args):
        super(Base, self).__init__(*args)
        name = str(self.__class__.__name__) # Class name.
        self.name = name
        # default template.
        self.templname = name + '.html'
        # default form.
        try:
            import forms
            self.forms[name] = eval('forms.' + name)
        except AttributeError:
            pass

    def render(self, formdict = None, **kwargs):
        forms = {}
        for key in self.forms:
            forms[key] = self.forms[key]() # Instance of form.
        if formdict:
            forms.update(formdict) # merger.
        super(Base, self).render(self.templname, forms = forms, **kwargs)

    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if not cookie:
            return False
        user_json = json.loads(cookie)
        user = Person.get_by(id=int(user_json['id']))
        if not user:
            return False
        return user

    def render_string(self, template_name, **methods):
        '''Template render by Jinja2.'''
        methods.update(
            {
                'xsrf': self.xsrf_form_html,
                'request': self.request,
                'settings': self.settings,
                'me': self.current_user,
                'static': self.static_url,
                'handler': self,
            }
        )
        methods.update(self.ui) # Enabled tornado UI methods.
        template = self.get_template(template_name)
        html = template.render(methods)
        return utils.remove_space(html) #remove space in line head and end.

    def get_template(self, template_name):
        '''Get jinja2 template object.'''
        env = Environment(
            # load template in file system.
            loader = FileSystemLoader(self.settings['template_path']), 
            auto_reload = self.settings['debug'], #auto reload
            autoescape = False, # auto escape
        )
        template = env.get_template(template_name)
        return template

    def get_error_html(self, status_code, **kwargs):
        if status_code == 404:
            return self.render_string('errors/404.html', **kwargs)
        else:
            self.write(str(status_code) + ' error')
        return

    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def redirect(self, path = None):
        if not path:
            path = self.get_argument("next", None)
            if not path:
                path = '/'
        super(Base, self).redirect(path)

    def getitem(self, Item, itemid):
        item = Item.get_by(id = int(itemid))
        if not item:
            raise web.HTTPError(404)
        return item 

    def form_loader(self, key = None):
        if not key:
            key = self.name
        form = self.forms[self.name]
        return form(self)

    def form_validate(self, form, key = None, **kwargs):
        if not key:
            key = self.name
        if not form.validate():
            self.render({key: form}, **kwargs)
            return False
        return True
