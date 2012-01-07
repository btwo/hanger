#!/usr/bin/env python2
# coding=utf-8
from view import Home, SignIn, SignUp, SignOut, PersonPage, Error404

handlers = [
    (r'/?', Home),
    (r'/sign/in/?', SignIn),
    (r'/sign/up/?', SignUp),
    (r'/sign/out/?', SignOut),
    (r'/person/(\d+)/?', PersonPage),
    (r'.*', Error404), #If url not belonging to any handler, raise 404error.
]
