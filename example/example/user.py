#!/usr/bin/env python2
# coding=utf-8
import os
import json
import StringIO
import Image
import uuid
import forms

from model import session, getuser, Person
from tornado import web
from hanger.send_mail import send_mail
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
        if "avatar" in self.request.files:
            new_avatar = self.request.files['avatar'][0]['body']
        else:
            new_avatar = None
        if new_name:
            me.name = new_name
        if new_bio:
            me.bio = new_bio
        if new_password:
            me.password = me.hash_password(new_password)
        if new_avatar:
            self.change_avatar(new_avatar)
        session.commit()
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

cache = {}

class UUIDCache(object):
    # TODO use redis.

    def generate(self, user):
        global cache
        key = uuid.uuid4()
        value = user.id
        cache[str(key)] = value
        return key

    def destroy(self, key):
        global cache
        del cache[key]

    def get(self, key):
        global cache
        try:
            return getuser(id = cache[key])
        except KeyError:
            return None

class ForgetPassword(Base):
    Form = forms.ForgetPassword

    def get(self):
        self.render()

    def post(self):
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user = getuser(email=form.email.data)
        key = UUIDCache().generate(user)
        self.send_mail(
            name = 'noreply',
            tolist = [form.email.data],
            subject = u"[%s]重置你的密码" % self.settings['site_name'],
            content = self.render_string('mail/reset_password' % key)
        )
        self.render(template_name = "mailed.html")


class ResetPassword(Base):
    Form = forms.ResetPassword

    def get(self, key):
        user = self.get_user(key)
        if not user:
            return
        self.render()

    def post(self, key):
        user = self.get_user(key)
        if not user:
            return
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user.password = user.hash_password(form.password.data)
        session.commit()
        self.redirect('/signin')

    def get_user(self, key):
        user = UUIDCache().get(key)
        if not user:
            web.HTTPError(404)
            return None
        else:
            return user


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
