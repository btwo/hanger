#!/usr/bin/env python2.7
# coding=utf-8
import os
import Image
import StringIO
import utils

SIZE = 256

def change_avatar(file_body, user, avatar_path):
    # TODO 128*128, 64*64, 32*32 size.
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
    height = SIZE
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

def avatar_url(url, user, size=SIZE):
    filename = user.avatar
    if filename == 'gravatar' or not filename:
        return utils.gravatar(user.email, size=size)
    return "%s/%s" % (url, filename)
