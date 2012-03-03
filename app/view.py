#!/usr/bin/env python2
# coding=utf-8
import os
import json
import StringIO
import Image

from base import Base
from model import getitem, Person
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
        person = getitem(Person, uid)
        print person
        self.render(person = person)


class Settings(Base):
    def __init__(self, *args):
        super(Settings, self).__init__(*args)
        self.form_add('ChangeAvatar')
        self.form_add('ChangePassword')
        self.form_add('ChangeName')

    @web.authenticated
    def get(self):
        self.render()
    
    @web.authenticated
    def post(self):
        new_password = self.form_loader('ChangePassword')
        new_name = self.form_loader('ChangeName')
        if self.request.files:
            self.avatar_uploads()
        elif new_password.password.data:
            self.change_password(new_password)
        elif new_name.name.data:
            self.change_name(new_name)
        self.redirect('')

    def change_name(self, form):
        #normal settings
        if not self.form_validate(form, 'ChangeName'):
            return
        self.current_user.change_name(form.name.data)
        session.commit()

    def change_password(self, form):
        if not self.form_validate(form, 'ChangePassword'): # change password.
            return
        self.current_user.change_password(form.new_password.data)
        session.commit()

    def avatar_uploads(self):
        form_key = 'ChangeAvatar'
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
        if not old_file:
            return
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
