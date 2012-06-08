#!/usr/bin/env python2.7
# coding=utf-8
from os.path import split
from config import config, ownpath, ad
filenames = ["conf/proxy.conf", "conf/redis.conf", "conf/supervisord.conf"]

# conver {{{key}}} to value in config files.
covers = [ 
    ("name", split(ownpath)[1]),
    ("path", ownpath),
    ("domain", config["site_domain"]),
    ("port", config["port"]),
    ("static_path", config["static_path"]),
    ("media_path", config["media_path"]),
    ("redis_db_filename", config["redis_db_filename"]),
    ("redis_logfile", config["redis_logfile"]),
    ("redis_port", config["redis_port"]),
]

for filename in filenames:
    raw_file_path = ad(filename+".temp")
    config_file_path = ad(filename)
    raw_file = open(raw_file_path, "r")
    configbody = raw_file.read()
    raw_file.close()
    config_file = open(config_file_path, "w")
    for cover in covers:
        configbody = configbody.replace("{{{%s}}}" % cover[0], str(cover[1]))
    config_file.write(configbody)
    config_file.close()

print "all done."
