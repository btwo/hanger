#!/usr/bin/env python2.7
# coding=utf-8
import utils
from avatar import avatar_url

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
    return avatar_url(handler.settings['avatar_url'], user, size)
