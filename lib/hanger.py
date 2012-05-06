#!/usr/bin/env python2 
# coding=utf-8 
import json

from tornado import web

class JinjaMixin(web.RequestHandler):
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

    def jinja_render(self, path, filename, **context):
        template = self.settings['jinja2_env'].get_template(filename)
        return template.render(**context)


class FormsDict(dict):
    def append(self, Form):
        self[Form.__name__] = Form()

class AutomationMixin(object):
    Form = None
    formset = []

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        self.templname = self.name + '.html'
        self.form_init()
        super(AutomationMixin, self).__init__(*args, **kwargs)

    def form_init(self):
        self.forms = FormsDict()
        if self.Form:
            self.forms.append(self.Form)
        for Form in self.formset:
            self.forms.append(Form)

    def form_loader(self, key=None, validate=True):
        if not key:
            try:
                form = self.Form(self)
            except TypeError:
                raise RuntimeError("Not set default form.")
        else:
            form = self.forms[key].__class__(self)
        if validate:
            if not self.form_validate(form):
                raise RuntimeError("form is not pass the validation.")
        return form

    def form_validate(self, form, **kwargs):
        '''Automated handle of Forms validate.'''
        if form.validate():
            return form
        self.render({form.__class__.__name__: form}, **kwargs)
        return False

    def render(self, forms=None, **context):
        if forms:
            self.forms.update(forms)
        super(AutomationMixin, self).render(
            self.templname, forms = self.forms, **context)


class BaseHandler(web.RequestHandler):
    '''
    Base handler is parent class of all handlers.
    had some tools for simpliy and enhancement base tornado web framework.
    '''
    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def redirect(self, url):
        url = self.get_argument("next", default = url)
        super(BaseHandler, self).redirect(url)
