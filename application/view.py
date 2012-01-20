#!/usr/bin/env python2
# coding=utf-8
import os
import json
import traceback
import httplib
import utils
import forms
import StringIO
import Image

from orm import Person, session
from jinja2 import Environment, FileSystemLoader
from tornado import web

class Base(web.RequestHandler):
    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if not cookie: return False
        user = json.loads(cookie)
        user = Person.get_by(id=int(user['id']))
        return user

    def render_string(self, template_name, **kwargs):
        '''Template render by Jinja2.'''
        methods = kwargs
        methods.update(
            {
                'xsrf': self.xsrf_form_html,
                'request': self.request,
                'settings': self.settings,
                'me': self.current_user,
                'url': self.settings['site_url'],
                'static': self.static_url,
                'handler': self,
            })
        methods.update(self.ui)
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
        code = status_code
        try:
            # add stack trace information
            message = httplib.responses[status_code]
            exception = "%s\n\n%s" % (kwargs["exception"],
                traceback.format_exc())
            template = "error.html"
            if code == 404: template = 'error_404.html'
            return self.render_string(
                template,
                code=code,
                message=message,
                exception=exception,
            )
        except Exception:
            return super(Base, self).get_error_html(status_code, **kwargs)

    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def redirect(self, to=None):
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


class Error404(Base):
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


class Sign(Base):
    def login(self, user):
        '''LogIn user to secure cookie'''
        json_str = json.dumps(
            {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            })
        self.set_secure_cookie("user", json_str)


class SignIn(Sign):
    Form = forms.SignIn
    templname = 'sign.in.html' #tamplate file name.

    def get(self):
        self.render(self.templname, form=self.Form())

    def post(self):
        form = self.Form(self)
        if not self.form_validate(form):
            return
        user = Person.get_by(email=form.email.data)
        self.login(user)
        self.redirect()


class SignUp(Sign):
    templname = 'sign.up.html'
    Form = forms.SignUp

    def get(self):
        self.render(self.templname, form=self.Form())
    
    def post(self):
        form = self.Form(self)
        if not self.form_validate(form):
            return
        user = Person(
            name = form.name.data,
            password = form.password.data,
            email = form.email.data,
        )
        session.commit()
        self.login(user)
        self.redirect()


class SignOut(Sign):
    def get(self):
        self.set_secure_cookie('user', '')
        self.redirect()


class PersonPage(Base):
    def get(self, uid=None):
        if uid:
            person = self.item(Person, int(uid))
        elif self.current_user:
            person = self.current_user
        else:
            raise web.HTTPError(404)
        self.render('person.page.html', person=person)


class Settings(Base):
    Form = forms.Settings
    AvatarForm = forms.Avatar
    templname = 'settings.html'

    @web.authenticated
    def get(self):
        self.render(self.templname, form=self.Form(),
            avatar_form = self.AvatarForm())
    
    @web.authenticated
    def post(self):
        form = self.Form(self)
        avatar_form = self.AvatarForm(self)
        if self.request.files:
            self.avatar_uploads(avatar_form)
            return
        #normal settings
        if self.form_validate(form, avatar_form = avatar_form):
            new_password = form.new_password.data
            name = form.name.data
            if new_password:
                self.current_user.password = utils.string_hash(new_password)
            if name:
                self.current_user.name = name
            session.commit()
            self.redirect()

    def avatar_uploads(self, avatar_form):
        if not self.form_validate(avatar_form):
            return
        avatar = Image.open(StringIO.StringIO(
            self.request.files['avatar'][0]['body']))
        self.remove_old_avatar()
        filename = self.avatar_save(avatar)
        self.current_user.avatar = filename
        session.commit()
        self.redirect('/settings')
        return
    
    def remove_old_avatar(self):
        old_file = self.current_user.avatar
        if old_file:
            os.remove(self.settings['avatar_path'] + old_file)

    def avatar_save(self, avatar):
        path = self.settings['avatar_path']
        uid = str(self.current_user.id)
        filename = uid + '.' + avatar.format
        avatar = self.avatar_resize(avatar)
        avatar.save(path + filename, avatar.format)
        return filename

    def avatar_resize(self, avatar):
        height = 160
        weight = height
        return avatar.resize((height, weight))


class Home(Base):
    def get(self):
        self.render('home.html')
