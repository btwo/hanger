#!/usr/bin/env python2
# coding=utf-8
import os
import json
import StringIO
import Image

from base import Base
from model import getuser, session, Person
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
        user = getuser(email = form.email.data)
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
        session.add(user)
        session.commit()
        self.login(user)
        self.redirect()


class SignOut(Sign):
    def get(self):
        self.set_secure_cookie('user', '')
        self.redirect()


class PersonPage(Base):
    def get(self, uid):
        person = getuser(uid)
        self.render(person = person)


class Settings(Base):
    def __init__(self, *args):
        super(Settings, self).__init__(*args)
        self.avatar_path = os.path.join(self.settings['static_path'], 'avatar')
        self.form_add('ChangeAvatar')
        self.form_add('ChangePassword')
        self.form_add('ChangeName')
        self.form_add('EditBio')

    @web.authenticated
    def get(self):
        self.render()
    
    @web.authenticated
    def post(self):
        new_password = self.form_loader('ChangePassword')
        new_name = self.form_loader('ChangeName')
        bio = self.form_loader('EditBio').bio.data
        if self.request.files:
            self.avatar_uploads()
        if new_password.password.data:
            self.change_password(new_password)
        if new_name.name.data:
            self.change_name(new_name)
        if bio:
            self.editbio(bio)
        self.redirect('/settings')

    def change_name(self, form):
        #normal settings
        if not self.form_validate(form, 'ChangeName'):
            return
        self.current_user.change_name(form.name.data)

    def change_password(self, form):
        if not self.form_validate(form, 'ChangePassword'): # change password.
            return
        self.current_user.change_password(form.new_password.data)

    def editbio(self, bio):
        self.current_user.change_bio(bio)

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
        return
    
    def remove_old_avatar(self):
        old_file = self.current_user.avatar
        if not old_file:
            return
        os.remove(os.path.join(self.avatar_path, old_file))

    def avatar_save(self, avatar):
        uid = str(self.current_user.id)
        filename = uid + '.' + avatar.format.lower()
        avatar = self.avatar_resize(avatar)
        save_path = os.path.join(self.avatar_path, filename)
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


class Redir(Base):
    def get(self):
        self.redirect()
