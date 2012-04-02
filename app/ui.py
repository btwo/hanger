#!/usr/bin/env python2
# coding=utf-8
import utils

def text2html(handler, text):
    '''Text to HTML.'''
    if not text: return ''
    text = utils.remove_space(text)
    html = ''
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        html += '<p>%s</p>\n' % paragraph
    return html

def field_maker(handler, field, class_ = None):
    '''WTForms field to HTML.'''
    label = field.label() + '<br>\n'
    field_html = field(class_ = class_)
    errors = field.errors
    html = ''
    html +=  label + field_html
    if errors:
        html += '\n<ul class="errors">\n'
        for error in errors:
            html += '\n<li class="error"><p>' + error + '<p></li>\n'
        html += '</ul>\n'
    html = '<p>' + html + '</p>\n'
    return html

def avatar(handler, user):
    avatar = user.avatar
    if (not avatar) or (avatar == 'gravatar'):
        return utils.gravatar(user.email)
    return handler.static_url('avatar/'+user.avatar)
