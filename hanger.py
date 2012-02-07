#!/usr/bin/env python2
# coding=utf-8
import sys
import os
import shutil

from optparse import OptionParser

def new_proj(projname, projpath):
    path = os.path.split(os.path.realpath(__file__))[0] + '/hanger'
    projpath = projpath + '/' + projname
    shutil.copytree(path, projpath)

def main():
    parser = OptionParser()
    parser.add_option('-n', '--new', action='store', dest='project_name',
        help='Create new project.')
    parser.add_option('-t', '--to', action='store', dest='project_path',
        help='New project path.')
    parser.add_option('-v', '--version', action='store_true', dest='version',
        default=False, help='Show the version of this command.')

    (options, args) = parser.parse_args(sys.argv)
    if options.project_name and options.project_path:
        new_proj(options.project_name, options.project_path)
    elif options.version:
        print '12.2.7'

if __name__ == '__main__':
    main()
