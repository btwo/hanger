#!/usr/bin/env python2.7
# coding=utf-8
import json

def get_config(path = "conf/config.json"):
    config_file = open(path)
    string = config_file.read()
    config = json.loads(unicode(string.decode("utf-8")))
    config_file.close()
    return config
