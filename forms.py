#!/usr/bin/env python2
# coding=utf-8
import wtforms
import orm
import lib

from wtforms.fields import TextField, TextField, PasswordField, TextAreaField
from wtforms.validators import Required, Length, Email, ValidationError

class MultiDict(object):
    '''Tornado handler arguments to MultiDice, wtforms required.'''
    def __init__(self, handler):
        self.handler = handler

    def __iter__(self):
        return iter(self.handler.request.arguments)

    def __len__(self):
        return len(self.handler.request.arguments)

    def __contains__(self, name):
        return (name in self.handler.request.arguments)

    def getlist(self, name):
        return self.handler.get_arguments(name, strip=False)


class Form(wtforms.Form):
    def __init__(self, handler=None):
        if handler:
            handler = MultiDict(handler)
        super(Form, self).__init__(formdata = handler)


class SignIn(Form):
    email = TextField(u'邮箱', [Required()])
    password = PasswordField(u'密码', [Required()])

    def validate_email(self, field):
        user = orm.Person.get_by(email = field.data)
        if not user:
            raise ValidationError(u'Email not found.')

    def validate_password(self, field):
        user = orm.Person.get_by(email=self.email.data)
        if not user: return
        password = lib.string_hash(field.data, user.salt)
        if not password == user.password:
            raise ValidationError(u'Password error.')
