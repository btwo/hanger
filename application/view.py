#!/usr/bin/env python2
# coding=utf-8
import json
import orm
import utils
import forms

from jinja2 import Environment, FileSystemLoader
from tornado import web

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
                'func': utils.UIFunc(),
                'me': self.current_user,
                'url': self.settings['site_url'],
                'static': self.static_url,
                'handler': self,
            })
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

    def redirect(self, to=None):
        if not to:
            to = self.get_argument("next", None)
            if not to: to = '/'
        super(Base, self).redirect(to)


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
    templname = 'sign.in.html' #tamplate file name.
    def get(self):
        self.render(self.templname, form=self.Form())

    def post(self):
        form = self.Form(self)
        if not form.validate():
            self.render(self.templname, form=form)
            return
        user = orm.Person.get_by(email=form.email.data)
        self.login(user)
        self.redirect()


class SignUp(Sign):
    templname = 'sign.up.html'
    Form = forms.SignUp

    def get(self):
        self.render(self.templname, form=self.Form())
    
    def post(self):
        form = self.Form(self)
        if not form.validate():
            self.render(self.templname, form=form)
            return
        user = orm.Person(
            name=form.name.data,
            password=form.password.data,
            email=form.email.data,
        )
        orm.session.commit()
        self.login(user)
        self.redirect()


class SignOut(Sign):
    def get(self):
        self.set_secure_cookie('user', '')
        self.redirect()


class Settings(Base):
    Form = forms.Settings
    templname = 'settings.html'

    @web.authenticated
    def get(self):
        self.render(self.templname, form=self.Form())
    
    @web.authenticated
    def post(self):
        form = self.Form(self)
        if not form.validate():
            self.render(self.templname, form = form)
