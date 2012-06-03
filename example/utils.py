#!/usr/bin/env python2.7
# coding=utf-8
import os
import json

from hanger.utils import realpath

def get_config(path = ""):
    if not path:
        path = os.path.join(realpath(__file__), "conf/config.json")
    config_file = open(path)
    string = config_file.read()
    config = json.loads(unicode(string.decode("utf-8")))
    config_file.close()
    return config
