#!/usr/bin/env python2
# coding=utf-8
import wtforms
import utils
import Image
import StringIO

from lib.forms import Form, EmailField
from model import getuser
from wtforms.fields import TextField, TextAreaField, PasswordField, FileField
from wtforms.validators import Required, Length, Email, ValidationError

def name_validate(self, field):
    if utils.special_char(field.data):
        raise ValidationError(u'昵称里面不允许有特殊字符。')
    elif getuser(name=field.data):
        raise ValidationError(u'Opps，这个昵称已经有人在用了。')

class SignIn(Form):
    email = EmailField(u'邮箱', [Required()])
    password = PasswordField(u'密码', [Required()])

    def validate_email(self, field):
        user = getuser(email = field.data)
        if not user:
            raise ValidationError(u'Email 没有找到。')

    def validate_password(self, field):
        user = getuser(email=self.email.data)
        if not user: return
        password = utils.string_hash(field.data, self.email.data)
        if password != user.password:
            raise ValidationError(u'Password error.')


class SignUp(Form):
    email = EmailField(u'Email',
        [Required(), Length(min=6), Length(max=120), Email()])

    name = TextField(u'称呼',
        [Required(), name_validate, Length(min=2), Length(max=18)])

    password = PasswordField(u'密码', [Required(), Length(min=8)])
    password_repeat = PasswordField(u'再输一遍密码', [Required()])

    def validate_email(self, field):
        if getuser(email=field.data):
            raise ValidationError(
                u'Email已存在，是否<a href="/signin/">登录</a>?')

    def validate_password(self, field):
        password = field.data
        password_repeat = self.password_repeat.data
        if password != password_repeat:
            raise ValidationError(u'Opps, 两次密码输入不一致')

class ChangePassword(Form):
    password = PasswordField(u'原密码', [Length(min = 6), Length(max = 30)])
    new_password = PasswordField(u'新密码',
        [Length(min = 6), Length(max = 30)])

    new_password_repeat = PasswordField(u'再输一遍', 
        [Length(min = 6), Length(max = 30)])

    def validate_password(self, field):
        current_user = self.handler.current_user
        if current_user.hash_password(field.data) != current_user.password:
            raise ValidationError(u'原密码输错了。')

    def validate_new_password(self, field):
        if field.data != self.new_password_repeat.data:
            raise ValidationError(u'两次密码输入的不一样。')


class ChangeName(Form):
    name = TextField(u'更改称呼',
        [name_validate, Length(max=10)])


class ChangeAvatar(Form):
    avatar = FileField(u'上传头像')

    def validate_avatar(self, field):
        filebody = self.handler.request.files['avatar'][0]['body']
        max_size = 1024 * 1024 #1Mb
        if len(filebody) > max_size:
            raise ValidationError(u'文件太大！最多只能上传1Mb的图片')
        try:
            Image.open(StringIO.StringIO(filebody))
        except IOError:
            raise ValidationError(u'这不是一个图片')


class EditBio(Form):
    bio = TextAreaField(u'简介', [Length(max=200)])
