#!/usr/bin/env python2 
# coding=utf-8 
import json
import traceback

from tornado import web, options
from jinja2 import Environment, FileSystemLoader
from send_mail import send_mail

class RequestHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self.handler_name = self.__class__.__name__
        super(RequestHandler, self).__init__(*args, **kwargs)


class JinjaMixin(RequestHandler):
    '''Use Jinja2 template engine.'''
    environment = None

    def __init__(self, *args, **kwargs):
        super(JinjaMixin, self).__init__(*args, **kwargs)
        if not JinjaMixin.environment:
            JinjaMixin.environment = Environment(
                # load template in file system.
                loader = FileSystemLoader(self.settings['template_path']),
                auto_reload = self.settings['debug'], #auto reload
                autoescape = False, # auto escape
            )

    def render_string(self, template_name, **context):
        context.update({
            'xsrf': self.xsrf_form_html,
            'request': self.request,
            'settings': self.settings,
            'me': self.current_user,
            'static': self.static_url,
            'domain': self.settings['site_domain'],
            'sitename': self.settings['site_name'],
            'handler': self,})
        context.update(self.ui) # Enabled tornado UI methods.
        return self.jinja_render(
            path = self.settings['template_path'],
            filename = template_name,
            auto_reload = self.settings['debug'], **context) #Render template.

    def jinja_render(self, path, filename, **context):
        template = self.environment.get_template(filename)
        return template.render(**context)


class FormsDict(dict):
    '''WTForms form object dict.'''
    def append(self, Form):
        self[Form.__name__] = Form()


class AutoTemplatesMixin(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(AutoTemplatesMixin, self).__init__(*args, **kwargs)
        self.template_name = "%s.html" % self.handler_name

    def render(self, **context):
        if not 'template_name' in context:
            context.update({'template_name': self.template_name})
        super(AutoTemplatesMixin, self).render(**context)


class AutoFormsMixin(RequestHandler):
    Form = None
    formset = []

    def __init__(self, *args, **kwargs):
        self.forms = FormsDict()
        if self.Form:
            self.forms.append(self.Form)
        for Form in self.formset:
            self.forms.append(Form)
        super(AutoFormsMixin, self).__init__(*args, **kwargs)

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

    def form_validate(self, form, *args, **kwargs):
        '''Automated handle of Forms validate.'''
        if form.validate():
            return form
        self.forms.update({form.__class__.__name__: form})
        self.render(*args, **kwargs)
        return False

    def render(self, template_name = "", **context):
        if not template_name:
            template_name = self.template_name
        super(AutoFormsMixin, self).render(
            template_name=template_name, forms=self.forms, **context)
        

class BaseHandler(RequestHandler):
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

    def send_error_mail(self, template_name, status_code, **kwargs):
        if not self.settings['send_error_mail']:
            return
        exception = "%s\n\n%s" % (
                kwargs["exception"], traceback.format_exc())
        self.send_mail(
            name = 'errorlog',
            to = self.settings['admin_mail'],
            subject = u"[%s]500 internal server error."\
                % self.settings['site_name'],
            content = self.render_string(
                template_name, exception=exception),
        )

    def send_mail(self, name, subject, content,
                  to=None, tolist=None, user=None, password=None):
        return send_mail(
            host = self.settings['mail_host'],
            name = name,
            postfix = self.settings['mail_postfix'],
            tolist = tolist,
            to = to,
            subject = subject,
            content = content,
            user = user,
            password = password,
        )
