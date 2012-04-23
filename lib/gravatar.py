#!/usr/bin/env python2
# coding=utf-8
import hashlib

def gravatar(email, size=200, default="identicon"):
    '''Make gravatar image URL.'''
    email = email.encode('utf-8').lower()
    email = hashlib.md5(email).hexdigest()
    url = "http://www.gravatar.com/avatar/%s/?s=%s&d=%s" % (
        email, str(size), default)
    return url
