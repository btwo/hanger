#!/usr/bin/env python2
# coding=utf-8

from hanger.utils import *

def password_hash(password, email):
    return string_hash(password, salt=email)
