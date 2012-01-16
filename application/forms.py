#!/usr/bin/env python2
# coding=utf-8
import wtforms
import orm
import utils
import Image
import StringIO

from orm import Person
from wtforms.fields import TextField, PasswordField, FileField
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
    handler = None
    def __init__(self, handler=None, **kwargs):
        formdata = None
        if handler:
            formdata = MultiDict(handler)
            self.handler = handler
        super(Form, self).__init__(formdata = formdata, **kwargs)


class SignIn(Form):
    email = TextField(u'邮箱', [Required()])
    password = PasswordField(u'密码', [Required()])

    def validate_email(self, field):
        user = Person.get_by(email = field.data)
        if not user:
            raise ValidationError(u'Email not found.')

    def validate_password(self, field):
        user = Person.get_by(email=self.email.data)
        if not user: return
        password = utils.string_hash(field.data)
        if not password == user.password:
            raise ValidationError(u'Password error.')


def name_validate(self, field):
    if utils.special_char(field.data):
        raise ValidationError(u'昵称里面不允许有特殊字符。')
    elif Person.get_by(name=field.data):
        raise ValidationError(u'Opps，这个昵称已经有人在用了。')

class SignUp(Form):
    email = TextField(u'Email',
        [Required(), Length(min=6), Length(max=120), Email()])
    name = TextField(u'称呼',
        [Required(), name_validate, Length(min=2), Length(max=18)])
    password = PasswordField(u'密码', [Required(), Length(min=8)])
    password_repeat = PasswordField(u'再输一遍密码', [Required()])

    def validate_email(self, field):
        if Person.get_by(email=field.data):
            raise ValidationError(
                u'有这个帐号，是否<a href="/signin/">登录</a>?')

    def validate_password(self, field):
        password = field.data
        password_repeat = self.password_repeat.data
        if password != password_repeat:
            raise ValidationError(u'Opps, 两次密码输入不一致')
        if utils.stupid_password(field.data):
            raise ValidationError(u'你的密码太简单了！')


class Settings(Form):
    name = TextField(u'更改称呼',
        [name_validate, Length(max=10)])
    password = PasswordField(u'原密码')
    new_password = PasswordField(u'新密码')
    new_password_repeat = PasswordField(u'再输一遍')

    def validate_password(self, field):
        password = field.data
        new_password = self.new_password.data
        if not new_password:
            return # not change password.
        elif utils.string_hash(password) != self.handler.current_user.password:
            raise ValidationError(u'原密码输错了。')

    def validate_new_password(self, field):
        if not field.data:
            return
        if len(field.data) < 8:
            raise ValidationError(u'密码太短啦')
        elif field.data != self.new_password_repeat.data:
            raise ValidationError(u'两次密码输入的不一样。')


class Avatar(Form):
    avatar = FileField(u'上传头像')

    def validate_avatar(self, field):
        max_size = 1024 * 1024 * 2 #2MB
        try:
            Image.open(StringIO.StringIO(
                self.handler.request.files['avatar'][0]['body']))
        except IOError:
            raise ValidationError(u'这不是一个图片')
        if len(field.data) > max_size:
            raise ValidationError(u'文件太大！最多只能上传2MB的图片')
