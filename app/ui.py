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

def avatar(handler, user):
    avatar = user.avatar
    if (not avatar) or (avatar == 'gravatar'):
        return utils.gravatar(user.email)
    return handler.static_url('avatar/'+user.avatar)
