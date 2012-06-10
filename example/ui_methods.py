#!/usr/bin/env python2.7
# coding=utf-8
import utils

from urlparse import urljoin

def text2html(handler, text):
    '''Text to HTML.'''
    if not text: return ''
    text = utils.remove_space(text)
    html = ''
    paragraphs = text.split('\n')
    for paragraph in paragraphs:
        html += '<p>%s</p>\n' % paragraph
    return html

def avatar(handler, user, size=256):
    filename = user.avatar
    if filename == 'gravatar' or not filename:
        return utils.gravatar(user.email, size=size)
    return urljoin(handler.settings['avatar_url'], filename)
