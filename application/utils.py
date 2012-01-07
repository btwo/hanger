#!/usr/bin/env python2
# coding=utf-8
import random
import hashlib
import re
import datetime
import os

from conf import settings

class UIFunc(object):
    def para(self, raw):
        '''Text to HTML.'''
        raw = raw.split('\n')
        result = ''
        for p in raw:
            p = p.strip()
            if p:
                result += '<p>' + p + '</p>\n' 
        return result


    def field_maker(self, field, class_=None):
        '''WTForms field to HTML.'''
        html = field.label() + '<br>' + field(class_=class_)
        if field.errors:
            html += '\n<ul class="errors">\n'
            for error in field.errors:
                html += '<li class="error"><p>' + error + '<p></li>\n'
            html += '</ul>\n'
        html = '<p>' + html + '</p>'
        return html


def realpath():
    '''Script real path.'''
    return os.path.split(os.path.realpath(__file__))[0]

def random_string(str_long = 40):
    return ''.join(random.sample([chr(i) for i in range(48, 123)], str_long))

def string_hash(string, salt=settings['hash_salt']):
    if salt:
        string += salt
    string = hashlib.sha224(string).hexdigest()
    return string

def escape(raw):
    '''Html escape.'''
    #todo: Not escape Escaped Char.
    escape_word = [
        ('&', '&amp;'),
        ('<', '&lt;'),
        ('>', '&gt;'),
        ('\"', '&quot;'),
        ('\'', '&apos;'),
    ]
    for word in escape_word:
        raw = raw.replace(word[0], word[1])
    return raw


def remove_space(raw):
    raw = raw.split('\n')
    result = ''
    for p in raw:
        p = p.strip()
        if p: result += p + '\n'
    return result

def special_char(string):
    '''find special char.'''
    string = unicode(string)
    regex = re.compile("\W",re.UNICODE)
    result = regex.search(string)
    return result

def gravatar(email, size="200", default="identicon"):
    '''Make gravatar image URL.'''
    email = email.encode('utf-8')
    email = hashlib.md5(email).hexdigest()
    url = "http://1.gravatar.com/avatar/%s?s=%s&d=%s&r=G" % (
        email, size, default)
    return url

def after(time):
    '''output time diffence.'''
    diff = datetime.datetime.now() - time
    if diff.days > 3:
        return strtime(time)
    elif diff.days > 0:
        return unicode(diff.days) + u'天前'
    elif diff.seconds > (60*60):
        return unicode(diff.seconds/(60*60)) + u'小时前'
    elif diff.seconds >= 60:
        return unicode(diff.seconds/60) + u'分钟前'
    elif diff.seconds > 20:
        return unicode(diff.seconds) + u'秒前'
    else:
        return u'此时'

def strtime(time, time_format="%y-%m-%d %H:%M"):
    return datetime.datetime.strftime(time, time_format)

def read_conf():
    pass
