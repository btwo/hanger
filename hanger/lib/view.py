#!/usr/bin/env python2
# coding=utf-8
import os
import json
import utils
import forms
import StringIO
import Image

from base import Base
from model import Person
from elixir import session
from tornado import web

class Sign(Base):
    def login(self, user):
        '''LogIn user to secure cookie'''
        json_obj = json.dumps(
            {
                'id': user.id,
                'name': user.name,
                'email': user.email,
            }
        )
        self.set_secure_cookie("user", json_obj)


class SignIn(Sign):
    def get(self):
        self.render()

    def post(self):
        form = self.form_loader()
        if not self.form_validate(form):
            return
        user = Person.get_by(email = form.email.data)
        self.login(user)
        self.redirect()


class SignUp(Sign):
    def get(self):
        self.render()
    
    def post(self):
        form = self.form_loader()
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
    def get(self, uid):
        person = self.getitem(Person, uid)
        self.render(person = person)


class Settings(Base):
    def __init__(self, *args):
        super(Settings, self).__init__(*args)
        self.forms['Avatar'] = forms.Avatar

    @web.authenticated
    def get(self):
        self.render()
    
    @web.authenticated
    def post(self):
        if self.request.files:
            self.avatar_uploads()
        else:
            self.do_set()
        return

    def do_set(self):
        #normal settings
        form = self.form_loader()
        if not self.form_validate(form):
            return
        new_password = form.new_password.data
        username = form.name.data
        if new_password: # change password.
            self.current_user.password = utils.string_hash(new_password)
        if username: # change name.
            self.current_user.name = username
        session.commit()
        self.redirect()

    def avatar_uploads(self):
        form_key = 'Avatar'
        form = self.form_loader(form_key)
        if not self.form_validate(form, form_key):
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
        avatar = avatar.resize((height, weight))
        return avatar


class Home(Base):
    def get(self):
        self.render()
