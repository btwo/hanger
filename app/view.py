#!/usr/bin/env python2
# coding=utf-8
import os
import json
import StringIO
import Image
import forms

from base import Base
from model import getuser, session, Person
from tornado import web

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
        self.render(person = person)


class Settings(Base):
    formset = [forms.ChangeAvatar, forms.ChangePassword, forms.ChangeName, 
               forms.EditBio,]

    @web.authenticated
    def get(self):
        self.render()
    
    @web.authenticated
    def post(self):
        try:
            change_password = self.form_loader('ChangePassword')
            change_name = self.form_loader('ChangeName')
            edit_bio = self.form_loader('EditBio')
            change_avatar = self.form_loader('ChangeAvatar')
        except RuntimeError:
            return
        if change_name.name.data:
            self.change_name(change_name)
        if edit_bio.bio.data:
            self.editbio(edit_bio)
        if change_password.new_password.data:
            self.change_password(change_password)
        if self.request.files:
            self.change_avatar(change_avatar)
        self.redirect('/settings')

    def change_name(self, form):
        #normal settings
        if not form:
            raise RuntimeError
        self.current_user.change_name(form.name.data)

    def change_password(self, form):
        if not form: # change password.
            raise RuntimeError
        self.current_user.change_password(form.new_password.data)

    def editbio(self, form):
        if not form:
            raise RuntimeError
        self.current_user.change_bio(form.bio.data)

    def change_avatar(self, form):
        if not form:
            raise RuntimeError
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
