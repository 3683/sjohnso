#!/usr/bin/env python

import os
import re
import sys
import getopt

self = os.path.basename(sys.argv[0])

file = ''
users = ''
help = False

def usage():
    print('\nUsage: %s [OPTION]... [OPTION]...' % self)
    print """
       --file
              file that has password information
              #server user clear_text_pass password_hash

       --users
              comma seperated listing of users

       --help
              display this help menu
"""
    sys.exit(2)

try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hf:u:', ['help', 'file=', 'users='])
except getopt.GetoptError as err:
    print(err)
    usage()

for opt, arg in options:
    if opt in ('-h', '--help'):
        help = True
    elif opt in ('-f', '--file'):
        file = arg
    elif opt in ('-u', '--users'):
        users = arg

## Sanity check
if help is True:
    usage()
if file == '':
    print('ERROR: Must provide the password file')
    usage()
if users == '':
    print('ERROR: Must provide the listing of users')
    usage()

users = re.split(',', users)

with open(file) as f:
    print('Server,User,Password')
    for line in f:
        s = re.split(' ', line.rstrip('\n'))
        if s[0] != '' and s[1] in users and s[2] != '':
            server = s[0]
            user = s[1]
            password = s[2]

            print('"%s","%s","%s"' % (server,user,password))

