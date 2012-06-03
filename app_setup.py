#!/usr/bin/env python2.7
# coding=utf-8
import os
import uuid

from os.path import join

def input():
    return raw_input("> ")

def get_path():
    print u"\n项目所在的路径（回车跳过则是当前目录）"
    print u"不包含项目名，可以使用相对路径"
    app_path = input()
    if not app_path:
        return os.path.split(os.path.realpath(__file__))[0]
    if not os.path.exists(app_path):
        if raw_input(
            u"目录不存在，是否创建？[Y/n]".encode("utf-8")).lower() == "n":
            return get_path()
        else:
            mkdir(app_path)
    return app_path 

def mkdir(path):
    try:
        os.mkdir(path)
        return
    except OSError: # mkdir error.
        if not os.access(path, os.W_OK):
            print u"错误！没有写权限，建议使用管理员权限运行此程序"
        else:
            print u"路径不可用，请重新输入。"
        return get_path()

def set_name():
    print u"\n项目英文名（使用于模块名 项目目录名等，使用英文小写字符)"
    app_name = input()
    if not app_name:
        print u"不能为空"
        return set_name()
    if " " in app_name:
        print u"错误，不允许有空格"
        return set_name()
    return app_name.lower()

def set_port(before="", default=8888):
    print u"\n%s端口" % before
    print u"不写则为默认: %d" % default
    port = input()
    if not port:
        return default
    try:
        port = int(port)
    except ValueError:
        print u"请输入一个数字"
        return set_port(before, default)
    if port > 65535:
        print u"端口号超出范围"
        return set_port(before, default)
    return port

def set_domain():
    print u"\n项目域名"
    print u"不加'http://'和'/'号。"
    print u"例如: eggfan.org www.foobar.com"
    domain = input()
    if not domain:
        print u"不能为空"
        return set_domain()
    return domain

def set_email():
    print u"\n输入管理员邮箱"
    email = input()
    if not email:
        print "不能为空"
    return email

def dir_changer(app_path, app_name):
    os.system("cp -rv example %s" % app_path)
    os.system("mv -v %s %s" % (
        join(app_path, "example"), join(app_path, app_name)))
    return

def file_changer(app_path, app_name, app_port, redis_port, app_domain,
                 admin_email):
    files = ['runserver.py', 'avatar_saver.py', 'dbinit.py',
             'conf/config.json', 'conf/proxy.conf', "conf/supervisord.conf",
             'conf/redis.conf']
    static_path = join(app_path, app_name, "static")
    template_path = join(app_path, app_name, "templates")
    logfile_path = join(app_path, "log", "application.log")
    redis_logfile_path = join(app_path, "log", "redis.log")
    redis_file_path = app_path
    for file_name in files:
        file_name = join(app_path, file_name)
        replace(file_name, [
            ("{{{app_path}}}", app_path),
            ("{{{app_static_path}}}", static_path),
            ("{{{app_template_path}}}", template_path),
            ("{{{app_name}}}", app_name),
            ("{{{app_port}}}", str(app_port)),
            ("{{{app_domain}}}", app_domain),
            ("{{{admin_mail}}}", admin_email),
            ("{{{logfile_path}}}", logfile_path),
            ("{{{redis_port}}}", str(redis_port)),
            ("{{{redis_db_file}}}", redis_file_path),
            ("{{{redis_logfile_path}}}", redis_logfile_path),
            ("{{{random_secret}}}", uuid.uuid4()),
        ])

def replace(file_name, replace_list):
    fil = open(file_name, 'r')
    file_body = fil.read()
    fil.close()
    for old, new in replace_list:
        file_body = file_body.replace(old, new)
    fil = open(file_name, 'w')
    fil.write(file_body)

def main():
    if not os.path.exists("example"):
        print "错误，当前目录下面没有example文件夹"
        exit()
    app_name = set_name()
    app_path = join(get_path(), app_name)
    app_port = set_port()
    redis_port = set_port("Redis", 6379)
    app_domain = set_domain()
    admin_email = set_email()
    dir_changer(app_path, app_name)
    file_changer(app_path, app_name, app_port, redis_port, app_domain,
                 admin_email)


if __name__ == '__main__':
    main()
