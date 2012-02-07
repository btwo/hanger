#!/usr/bin/env python2
# coding=utf-8
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-n', '--new', action='store', dest='project_name',
    help='Create new project.')
parser.add_option('-v', '--version', action='store_true', dest='version',
    default=False, help='Show the version of this command.')

(options, args) = parser.parse_args(sys.argv)
if options.project_name:
    print options.project_name
elif options.version:
    print '12.2.7'
