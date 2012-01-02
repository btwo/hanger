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


class SignUp(Form):
    email = TextField(u'Email',
        [Required(), Length(min=6), Length(max=120), Email()])
    name = TextField(u'称呼',
        [Required(), Length(min=2), Length(max=10)])
    password = PasswordField(u'密码', [Required(), Length(min=8)])
    password_repeat = PasswordField(u'再输一遍密码',
        [Required()])

    def validate_email(self, field):
        if orm.Person.get_by(email=field.data):
            raise ValidationError(
                u'有这个帐号，是否<a href="/signin/">登录</a>?')

    def validate_name(self, field):
        if lib.special_char(field.data):
            raise ValidationError(u'昵称里面不允许有特殊字符。')
        elif orm.Person.get_by(name=field.data):
            raise ValidationError(u'Opps，这个昵称已经有人在用了。')

    def validate_password(self, field):
        password = field.data
        password_repeat = self.password_repeat.data
        if password != password_repeat:
            raise ValidationError(u'Opps, 两次密码输入不一致')
