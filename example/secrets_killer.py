#!/usr/bin/env python2.7
# coding=utf-8
import time

from utils import get_config
from redis import StrictRedis

def killer(redis):
    listname = "secret_key"
    swap_list = []
    while True:
        secret = redis.lpop(listname)
        if not secret: # list empty.
            break
        life_key = "%s:life" % secret
        # Get infomation.
        life = redis.get(life_key)
        # if life < now time: the secret is too old.
        if float(life) > time.time():
            # Health 
            swap_list.append(secret)
            break # the list is new -> old, if thishealth, before health too.
        else:
            # Died
            redis.delete(life_key)
            redis.delete("%s:user_id" % secret)
    if swap_list:
        redis.lpush(listname, *swap_list)

def main():
    config = get_config()
    redis = StrictRedis(
        host='localhost', port=config['redis_port'], db=config['redis_db'])
    while True:
        killer(redis)
        time.sleep(60 * 30)

if __name__ == "__main__":
    main()
