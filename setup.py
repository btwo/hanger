#!/usr/bin/env python2
# coding=utf-8
'''
A framework for simpliy web application programming, base on tornado.
'''
from setuptools import setup

setup(
    name='Hanger',
    version='0.6',
    url='http://github.com/tioover/hanger/',
    license='MIT',
    author='tioover',
    author_email='tioover@gmail.com',
    description='Hanger web framework.',
    long_description=__doc__,
    packages=['hanger'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Tornado',
        'Jinja2',
        'WTForms',
        'SQLAlchemy',
        'PIL',
        'Elixir',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
