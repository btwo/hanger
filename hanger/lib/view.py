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

class Error404(Base):
    def get(self):
        raise web.HTTPError(404)

    def post(self):
        raise web.HTTPError(404)


class Sign(Base):
    def login(self, user):
        '''LogIn user to secure cookie'''
        json_obj = json.dumps(
            {'id': user.id,
            'name': user.name,
            'email': user.email,}
        )
        self.set_secure_cookie("user", json_obj)


class SignIn(Sign):
    Form = forms.SignIn
    templname = 'SignIn.html' #tamplate file name.

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
    templname = 'SignUp.html'
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
    def get(self, uid):
        person = self.item(Person, int(uid))
        self.render('PersonPage.html', person=person)


class Settings(Base):
    Form = forms.Settings
    AvatarForm = forms.Avatar
    templname = 'Settings.html'

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
        if not avatar_form.validate():
            self.render(
                self.templname, form = self.Form(), avatar_form = avatar_form)
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
        self.render('Home.html')
