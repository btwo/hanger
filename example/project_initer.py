#!/usr/bin/env python2.7
# coding=utf-8
'''Edit some config file.'''
from config import config, ownpath, ad, dirname, upload_config
filenames = ["conf/proxy.conf", "conf/redis.conf", "conf/supervisord.conf"]

# conver {{{key}}} to value in config files.
covers = [ 
    ("name", dirname),
    ("path", ownpath),
    ("domain", config["site_domain"]),
    ("port", config["port"]),
    ("static_path", config["static_path"]),
    ("media_path", config["media_path"]),
    ("redis_db_filename", config["redis_db_filename"]),
    ("redis_logfile", config["redis_logfile"]),
    ("redis_port", config["redis_port"]),
    ("upload_store", upload_config["store"]),
    ("upload_max_size", upload_config["max_size"]),
    ("upload_limit", upload_config["limit"]),
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
