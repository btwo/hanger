#!/usr/bin/env python2.7
# coding=utf-8
'''avatar file operations.'''
import os
import Image
import StringIO

def change_avatar(file_body, user, avatar_path):
    try:
        avatar = avatar_load(file_body)
    except IOError:
        return ""
    remove_old(user, avatar_path)
    filename = save(avatar, user, avatar_path)
    change_user_data(user, filename)
    return

def avatar_load(file_body):
    return Image.open(StringIO.StringIO(file_body))

def remove_old(user, path):
    old_file = user.avatar
    if not old_file:
        return
    try:
        os.remove(os.path.join(path, old_file))
    except OSError:
        pass

def resize(avatar):
    height = 160
    weight = height
    return avatar.resize((height, weight), Image.ANTIALIAS)

def save(avatar, user, path):
    filename = "%d.%s" % (user.id, avatar.format.lower())
    save_path = os.path.join(path, filename)
    avatar = resize(avatar)
    avatar.save(save_path, avatar.format)
    return filename

def change_user_data(user, filename):
    user.avatar = filename
