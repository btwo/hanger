#!/usr/bin/env python2.7
# coding=utf-8
import os
import json
import StringIO
import Image
import uuid
import forms
import time
import avatar

from model import session, getuser, Person
from tornado import web
from base import Base

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
    def get(self, user_id):
        person = getuser(id=user_id)
        if not person:
            raise web.HTTPError(404)
        self.render(person = person)


class Settings(Base):
    Form = forms.Settings

    @web.authenticated
    def get(self):
        form = self.forms['Settings']
        form.bio.data = self.current_user.bio
        form.name.data = self.current_user.name
        self.render()
    
    @web.authenticated
    def post(self):
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        me = self.current_user
        new_name = form.name.data
        new_bio = form.bio.data
        new_password = form.new_password.data
        new_avatar = None
        if "avatar" in self.request.files:
            new_avatar = self.request.files['avatar'][0]['body']

        if new_name:
            me.name = new_name
        if new_bio:
            me.bio = new_bio
        if new_password:
            me.password = me.hash_password(new_password)
        if new_avatar:
            avatar.change_avatar(
                new_avatar, self.current_user, self.settings['avatar_path'])
        session.commit()
        self.redirect('/settings')


class ResetBase(Base):
    def secret_init(self, user):
        hour = 60 * 60
        life = time.time() + (hour)
        key = str(uuid.uuid4())
        self.redis.lpush("secret_key", key) # add new key in list head.
        self.redis.set("%s:user_id" % key, user.id)
        self.redis.set("%s:life" % key, life)
        return key

    def secret_destroy(self, key):
        self.redis.delete("%s:user_id" % key)

    def secret_get(self, key):
        try:
            user_id = int(self.redis.get("%s:user_id"%key))
        except TypeError: # not get value.
            return None
        try:
            return getuser(id = user_id)
        except KeyError:
            return None


class ForgetPassword(ResetBase):
    Form = forms.ForgetPassword

    def get(self):
        self.render()

    def post(self):
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user = getuser(email=form.email.data)
        key = self.secret_init(user)
        sent = self.send_mail(
            name = 'noreply',
            to = form.email.data,
            subject = u"[%s]重置你的密码" % self.settings['site_name'],
            content = self.render_string('mail/reset_password', key=key)
        )
        print key
        if sent:
            self.render(template_name = "mailed.html")
        else:
            self.render(template_name = "mailnotsent.html")


class ResetPassword(ResetBase):
    Form = forms.ResetPassword

    def get(self, key):
        user = self.secret_get(key)
        if not user:
            raise web.HTTPError(404)
        self.render()

    def post(self, key):
        user = self.secret_get(key)
        if not user:
            raise web.HTTPError(404)
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user.password = user.hash_password(form.password.data)
        session.commit()
        self.secret_destroy(key)
        self.redirect('/signin')


uuid_regex = "[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}"
routes = [
    (r'/signin/?', SignIn),
    (r'/signup/?', SignUp),
    (r'/signout/?', SignOut),
    (r'/person/(\d+)/?', PersonPage),
    (r'/settings/?', Settings),
    (r'/forget_password/?', ForgetPassword),
    (r'/reset_password/(%s)/?' % uuid_regex, ResetPassword),
]
