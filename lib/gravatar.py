#!/usr/bin/env python2
# coding=utf-8
import hashlib

def gravatar(email, size="200", default="identicon"):
    '''Make gravatar image URL.'''
    email = email.encode('utf-8')
    email = hashlib.md5(email).hexdigest()
    url = "http://www.gravatar.com/%s/avatar/?s=%s&d=%s&r=G" % (
        email, size, default)
    return url
