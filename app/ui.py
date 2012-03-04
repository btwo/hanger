#!/usr/bin/env python2
# coding=utf-8
import utils

def texttohtml(handler, text):
    '''Text to HTML.'''
    text = utils.remove_space(text)
    html = ''
    para_list = text.split('\n')
    for para in para_list:
        html += '<p>%s</p>\n' % para
    return html

def field_maker(handler, field, class_ = None, show_label = True):
    '''WTForms field to HTML.'''
    html = ''
    label = ''
    if show_label:
        label = field.label() + '<br>\n'
    field_html = field(class_ = class_)
    errors = field.errors
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
