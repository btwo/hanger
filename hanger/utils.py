#!/usr/bin/env python2.7
# coding=utf-8
'''
Some project helper functions.
'''
import os
import re
import random
import hashlib
import datetime
import markdown2

from tornado.escape import xhtml_unescape, xhtml_escape

def realpath(file_):
    '''file local path.'''
    return os.path.split(os.path.realpath(file_))[0]

def escape(raw):
    '''Html escape.'''
    return xhtml_escape(xhtml_unescape(raw))

def random_string(length = 40):
    string = ''.join(random.sample([chr(i) for i in range(48, 123)], length))
    string.replace("\\", "/")
    return string

def string_hash(string, salt=""):
    string = hashlib.sha224(salt + string).hexdigest()
    return string

def remove_space(raw):
    '''remove space in line start and end.'''
    result = ''
    for part in raw.split('\n'):
        part = part.strip()
        if not part: continue
        result += part + '\n'
    return result

def after(time):
    '''output time diffence.'''
    diff = datetime.datetime.now() - time
    if diff.days > 3:
        return strtime(time)
    elif diff.days > 0:
        return unicode(diff.days) + u'天前'
    elif diff.seconds > (60*60):
        return unicode(diff.seconds / (60*60)) + u'小时前'
    elif diff.seconds >= 60:
        return unicode(diff.seconds / 60) + u'分钟前'
    elif diff.seconds > 5:
        return unicode(diff.seconds) + u'秒前'
    return u'此时'
    
def strtime(time, time_format="%y-%m-%d %H:%M"):
    return datetime.datetime.strftime(time, time_format)

def mdtohtml(raw):
    """Markdown to HTML."""
    raw = raw.replace("\n&gt;", "\n>")
    md = markdown2.Markdown()
    html = md.convert(raw)
    return html

def special_char(string):
    '''find special char.'''
    string = unicode(string)
    regex = re.compile("\W", re.UNICODE)
    result = regex.search(string)
    return result

def gravatar(email, size=200, default="identicon"):
    '''Make gravatar image URL.'''
    email = email.encode('utf-8').lower()
    email = hashlib.md5(email).hexdigest()
    url = "http://www.gravatar.com/avatar/%s/?s=%s&d=%s" % (
        email, str(size), default)
    return url
