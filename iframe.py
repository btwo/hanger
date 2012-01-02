#!/usr/bin/env python2
# coding=utf-8
import json
import elixir
import orm
import lib
import forms

from tornado import web, options, httpserver, ioloop
from jinja2 import Environment, FileSystemLoader

class Base(web.RequestHandler):
    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if not cookie: return False
        user = json.loads(cookie)
        user = orm.Person.get_by(id=int(user['id']))
        return user

    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def render_string(self, template_name, **kwargs):
        '''Template render by Jinja2.'''
        methods = kwargs
        methods.update(
            {
                'xsrf': self.xsrf_form_html,
                'request': self.request,
                'settings': self.settings,
                'func': lib.UIFunc(),
                'me': self.current_user,
                'url': settings['site_url'],
                'static': self.static_url,
            })
        template = self.get_template(template_name)
        html = template.render(methods)
        return lib.remove_space(html)

    def get_template(self, template_name):
        '''Get jinja2 template object.'''
        env = Environment(
            loader = FileSystemLoader(self.settings['template_path']),
            auto_reload = self.settings['debug'],
            autoescape = False,
        )
        template = env.get_template(template_name)
        return template

    def redir(self, to=None):
        if not to:
            to = self.get_argument("next", None)
            if not to: to = '/'
        self.redirect(to)


class Home(Base):
    def get(self):
        self.render('home.html')


class Sign(Base):
    def login(self, user):
        '''LogIn user to secure cookie'''
        json_str = json.dumps(
            {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            }
        )
        self.set_secure_cookie("user", json_str)


class SignIn(Sign):
    Form = forms.SignIn
    tempname = 'sign.in.html' #tamplate file name.
    def get(self):
        self.render(self.tempname, form=self.Form())

    def post(self):
        form = self.Form(self)
        if not form.validate():
            self.render(self.tempname, form=form)
            return
        user = orm.Person.get_by(email=form.email.data)
        self.login(user)
        self.redir()


class SignUp(Sign):
    def get(self):
        self.render('sign.up.html')


class SignOut(Sign):
    @web.authenticated
    def get(self):
        self.set_secure_cookie('user', '')
        self.redir()


settings = dict(
    #Site and application settings.
    debug = True,
    template_path = './templates',
    static_path = './static',
    login_url = '/sign/in/',
    site_url = 'http://127.0.0.1:8888',
    xsrf_cookies = True,
    cookie_secret = r'ThisIsTheCookieSecret_2012/1/2/16:37.',
    port = 8888,
)


handlers = [
    (r'/?', Home),
    (r'/sign/in/?', SignIn),
    (r'/sign/up/?', SignUp),
    (r'/sign/out/?', SignOut),
]

app = web.Application(handlers, **settings)

def server_run():
    elixir.setup_all() #ORM setup.
    if settings['debug']: options.parse_command_line() #CMD Log
    http_server = httpserver.HTTPServer(app) #Server
    http_server.listen(settings['port']) # Port
    ioloop.IOLoop.instance().start() #Start IO Loop

if __name__ == '__main__': server_run()
