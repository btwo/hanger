#!/usr/bin/env python2
# coding=utf-8
import wtforms
import utils
import Image
import StringIO

from wtforms.fields import TextField, PasswordField, FileField
from wtforms.validators import Required, Length, Email, ValidationError

class TornadoArgumentsWrapper(object):
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
    def __init__(self, formdata = None, **kwargs):
        if formdata:
            self.handler = formdata
            formdata = TornadoArgumentsWrapper(formdata)
        super(Form, self).__init__(formdata = formdata, **kwargs)
