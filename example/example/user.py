#!/usr/bin/env python2
# coding=utf-8
import os
import json
import StringIO
import Image
import uuid
import forms
import socket

from model import session, getuser, Person
from tornado import web, ioloop
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

def sent_avatar(self, path, avatar):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 53333))
    sock.send(json.dumps({'path':path, 'avatar':avatar}))
    sock.close()


class UUIDCache(object):
    # TODO use redis.
    cache = {}

    def generate(self, user):
        key = uuid.uuid4()
        value = user.id
        self.cache[str(key)] = value
        return key

    def destroy(self, key):
        del self.cache[key]

    def get(self, key):
        try:
            return getuser(id = self.cache[key])
        except KeyError:
            return None

    def clear(self):
        self.cache = {}

cache = UUIDCache()


class ForgetPassword(Base):
    Form = forms.ForgetPassword

    def get(self):
        self.render()

    def post(self):
        global cache
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user = getuser(email=form.email.data)
        key = cache.generate(user)
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


class ResetPassword(Base):
    Form = forms.ResetPassword

    def get(self, key):
        global cache
        user = cache.get(key)
        if not user:
            raise web.HTTPError(404)
        self.render()

    def post(self, key):
        global cache
        user = cache.get(key)
        if not user:
            raise web.HTTPError(404)
        try:
            form = self.form_loader()
        except RuntimeError:
            return
        user.password = user.hash_password(form.password.data)
        session.commit()
        cache.destroy(key)
        self.redirect('/signin')

def clear_uuid():
    '''Remove all key.'''
    global cache
    cache.clear()

one_day = 24 * 60 * 60 * 1000
ioloop.PeriodicCallback(
    clear_uuid, one_day).start() # remove all key each day.

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
