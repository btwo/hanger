#!/usr/bin/env python2
# coding=utf-8
import random
import hashlib
import re

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


def random_string(str_long = 40):
    return ''.join(random.sample([chr(i) for i in range(48, 123)], str_long))

def string_hash(string, salt=None):
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
    regex = re.compile("\W",re.UNICODE)
    result = regex.search(string)
    return result
