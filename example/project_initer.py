#!/usr/bin/env python2.7
# coding=utf-8
from config import config, ad

files = [ad(path) for path in ["conf/proxy.conf", "conf/redis.conf",
                               "conf/supervisord.conf"]]

# conver {{{key}}} to value in config files.
covers = [ 
    ("domain", config["site_domain"]),
    ("port", config["port"]),
    ("static_path", config["static_path"]),
    ("media_path", config["media_path"]),
    ("redis_db_file", config["redis_db_file"]),
    ("redis_logfile", config["redis_logfile"]),
    ("redis_port", config["redis_port"]),
]

for filename in files:
    configfile = open(filename, "r")
    configbody = configfile.read()
    configfile.close()
    configfile = open(filename, "w")
    for cover in covers:
        configbody.replace(cover[0], cover[1])
    configfile.write(configbody)
    configfile.close()

print "all done."
