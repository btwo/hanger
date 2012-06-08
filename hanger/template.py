#!/usr/bin/env python2.7
# coding=utf-8 
from jinja2 import Environment, FileSystemLoader

class AutoTemplatesMixin(object):
    autoload_template = True
    def __init__(self, *args, **kwargs):
        super(AutoTemplatesMixin, self).__init__(*args, **kwargs)
        if self.autoload_template:
            self.template_name = "%s.html" % self.handler_name

    def render(self, **context):
        if 'template_name' not in context and self.autoload_template:
            context.update({'template_name': self.template_name})
        super(AutoTemplatesMixin, self).render(**context)


class JinjaMixin(object):
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
