#!/usr/bin/env python2
# coding=utf-8
import utils

def para(handler, raw):
    '''Text to HTML.'''
    raw = raw.split('\n')
    result = ''
    for p in raw:
        p = p.strip()
        if p:
            result += '<p>' + p + '</p>\n' 
    return result

def field_maker(handler, field, class_=None):
    '''WTForms field to HTML.'''
    html = field.label() + '<br>\n' + field(class_=class_)
    if field.errors:
        html += '\n<ul class="errors">\n'
        for error in field.errors:
            html += '\n<li class="error"><p>' + error + '<p></li>\n'
        html += '</ul>\n'
    html = '<p>' + html + '</p>\n'
    return html

def avatar(handler, user):
    avatar = user.avatar
    if (not avatar) or (avatar == 'gravatar'):
        return utils.gravatar(user.email)
    else:
        return handler.static_url('avatar/'+user.avatar)

def gravatar(handler, user):
    return utils.gravatar(user.email)
