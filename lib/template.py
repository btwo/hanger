#!/usr/bin/env python2
# coding=utf-8
from jinja2 import Environment, FileSystemLoader

def render(path, filename, auto_reload=False, autoescape=False,
                  **context):
    env = Environment(
        # load template in file system.
        loader = FileSystemLoader(path),
        auto_reload = auto_reload, #auto reload
        autoescape = False, # auto escape
    )
    template = env.get_template(filename)
    return template.render(**context)
