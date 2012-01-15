#!/usr/bin/env python2
# coding=utf-8
import random
import hashlib
import re
import datetime
import os
import markdown2
import tornado.escape

from conf import settings

def realpath():
    '''Script real path.'''
    return os.path.split(os.path.realpath(__file__))[0]

def escape(raw):
    '''Html escape.'''
    #todo: Not escape Escaped Char.
    raw = tornado.escape.xhtml_unescape(raw)
    raw = tornado.escape.xhtml_escape(raw)
    return raw


def url_escape(url):
    url = tornado.escape.url_escape(url)
    return url


def random_string(str_long = 40):
    return ''.join(random.sample([chr(i) for i in range(48, 123)], str_long))

def string_hash(string, salt=settings['hash_salt']):
    string = hashlib.sha224(string).hexdigest()
    return string

def stupid_password(password):
    '''look here http://coolshell.cn/articles/6193.html .'''
    stupid_password_list = [
        '123456789',
        '12345678',
        'dearbook',
        '123123123',
        '1234567890',
        '147258369',
        '987654321',
    ]
    clean = list(set(password)) # 如果是 aaaaaaa这样的密码，就会返回['a']
    if password in stupid_password_list or len(clean) is 1:
        return True
    else: return False

def remove_space(raw):
    '''清除首位空格'''
    raw = raw.split('\n')
    result = ''
    for p in raw:
        p = p.strip()
        if p: result += p + '\n'
    return result

def special_char(string):
    '''find special char.'''
    string = unicode(string)
    regex = re.compile("\W", re.UNICODE)
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

def mdtohtml(raw):
    """将markdown格式文本转换为HTML"""
    #解决转义和markdown格式的冲突
    raw = raw.replace("&gt;", "\n>")
    #开始转换
    md = markdown2.Markdown()
    html = md.convert(raw)
    return html
