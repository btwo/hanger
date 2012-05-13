#!/usr/bin/env python2
# coding=utf-8
import os
import json
import StringIO
import Image
import forms

from model import getuser, session, Person
from tornado import web
from lib.hanger import BaseHandler, JinjaMixin, AutomationMixin

class Base(AutomationMixin, JinjaMixin, BaseHandler):
    def get_error_html(self, status_code, **kwargs):
        try:
            return self.render_string('errors/%d.html' % status_code, **kwargs)
        except:
            self.set_header('Content-Type', 'text/plan')
            return "Sorry, an %d HTTP Error has occurred." % status_code

    def get_current_user(self):
        cookie = self.get_secure_cookie('user')
        if not cookie:
            return None
        user = getuser(json.loads(cookie)['id'])
        if user:
            return user


class PageNotFound(Base):
    '''If url not belonging to any handler, raise 404error.'''
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


class Sign(Base):
    def login(self, user):
        '''LogIn user to secure cookie'''
        json_obj = json.dumps({
            'id': user.id,
            'name': user.name,
            'email': user.email,
        })
        self.set_secure_cookie("user", json_obj)


class SignIn(Sign):
    Form = forms.SignIn
    def get(self):
        self.render()

    def post(self):
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user = getuser(email = form.email.data)
        self.login(user)
        self.redirect('/')


class SignUp(Sign):
    Form = forms.SignUp

    def get(self):
        self.render()
    
    def post(self):
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user = Person(
            name = form.name.data,
            password = form.password.data,
            email = form.email.data,
        )
        session.add(user)
        session.commit()
        self.login(user)
        self.redirect('/')


class SignOut(Sign):
    def get(self):
        self.set_secure_cookie('user', '')
        self.redirect('/')


class PersonPage(Base):
    def get(self, uid):
        person = getuser(uid)
        if not person:
            raise web.HTTPError(404)
        self.render(person = person)


class Settings(Base):
    Form = forms.Settings

    @web.authenticated
    def get(self):
        self.render()
    
    @web.authenticated
    def post(self):
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        new_name = form.name.data
        new_bio = form.bio.data
        new_password = form.new_password.data
        if "avatar" in self.request.files:
            new_avatar = self.request.files['avatar'][0]['body']
        else:
            new_avatar = None
        if new_name:
            self.current_user.change_name(new_name)
        if new_bio:
            self.current_user.change_bio(new_bio)
        if new_password:
            self.current_user.change_password(new_password)
        if new_avatar:
            self.change_avatar(new_avatar)
        self.redirect('/settings')

    def change_avatar(self, new_avatar):
        avatar = Image.open(StringIO.StringIO(new_avatar))
        self.remove_old_avatar()
        filename = self.avatar_save(avatar)
        self.current_user.avatar = filename
        return
    
    def remove_old_avatar(self):
        old_file = self.current_user.avatar
        if not old_file:
            return
        os.remove(os.path.join(self.settings['avatar_path'], old_file))

    def avatar_save(self, avatar):
        uid = str(self.current_user.id)
        filename = uid + '.' + avatar.format.lower()
        avatar = self.avatar_resize(avatar)
        save_path = os.path.join(self.settings['avatar_path'], filename)
        avatar.save(save_path, avatar.format)
        return filename

    def avatar_resize(self, avatar):
        height = 160
        weight = height
        avatar = avatar.resize((height, weight))
        return avatar


class Home(Base):
    def get(self):
        self.render()
