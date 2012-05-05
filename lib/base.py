#!/usr/bin/env python2 
# coding=utf-8 
import json

from app import forms
from tornado import web
from jinja2 import Environment, FileSystemLoader

class JinjaMixin(object):
    def render_string(self, template_name, **context):
        '''Template render by Jinja2.'''
        default_context = {
            'xsrf': self.xsrf_form_html,
            'request': self.request,
            'settings': self.settings,
            'me': self.current_user,
            'static': self.static_url,
            'handler': self,
        }
        context.update(default_context)
        context.update(self.ui) # Enabled tornado UI methods.
        return self.jinja_render(
            path = self.settings['template_path'],
            filename = template_name,
            auto_reload = self.settings['debug'],
            **context) #Render template.

    def jinja_render(self, path, filename, auto_reload=False, autoescape=False,
                      **context):
        env = Environment(
            # load template in file system.
            loader = FileSystemLoader(path),
            auto_reload = auto_reload, #auto reload
            autoescape = False, # auto escape
        )
        template = env.get_template(filename)
        return template.render(**context)


class Base(web.RequestHandler):
    '''
    Base handler is parent class of all handlers.
    had some tools for simpliy and enhancement base tornado web framework.
    '''
    name = "" # class name.
    forms_name = [] # Key, for autoload forms.
    forms = {} # wtform obj dict.
    templname = '' # template file name.

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.db = self.application.session
        self.name = str(self.__class__.__name__) # class name
        self.forms_name.append(self.name)
        self.__forms_add() # register default forms.
        self.templname = self.name + '.html' # default template file name.

    def form_loader(self, key = None):
        '''
        Get form in forms dict.
        '''
        if not key:
            key = self.name
        form = self.forms[key]
        return form(self)

    def __form_add(self, form_name):
        '''Register form to self.forms. '''
        try:
            form = eval('forms.' + form_name)
            self.forms[form_name] = form
        except AttributeError:
            form = None
        return form

    def __forms_add(self):
        for name in self.forms_name:
            self.__form_add(name)

    def form_validate(self, form, key = None, **kwargs):
        '''Automated handle of Forms validate.'''
        if not key:
            key = self.name # default form key.
        if not form.validate():
            self.render({key: form}, **kwargs)
            return False
        return True

    def render(self, formobj_dict = None, **kwargs):
        '''Render templates and auto load forms.'''
        # Auto load form.
        formdict = {}
        for key in self.forms:
            formdict[key] = self.forms[key]() # Instance of form.
        if formobj_dict:
            formdict.update(formobj_dict) # merger.
        super(Base, self).render(self.templname, forms = formdict,
                                 **kwargs)
    def get_error_html(self, status_code, **kwargs):
        code = str(status_code)
        try:
            return self.render_string('errors/'+code+'.html', **kwargs)
        except:
            self.write('Sorry, happen an error.')

    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def redirect(self, url, *args):
        url = self.get_argument("next", None)
        super(Base, self).redirect(url, *args)
