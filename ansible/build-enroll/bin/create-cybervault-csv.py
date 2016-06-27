#!/usr/bin/env python

import os
import re
import sys
import getopt

self = os.path.basename(sys.argv[0])

file = ''
abbrev = ''
users = ''
help = False

def usage():
    print('\nUsage: %s [OPTION]... [OPTION]...' % self)
    print """
       --file
              file that has password information
              #server user clear_text_pass password_hash

       --abbrev
              customer abbreviation

       --users
              comma seperated listing of users

       --help
              display this help menu
"""
    sys.exit(2)

try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hf:a:u:', ['help', 'file=', 'abbrev=', 'users='])
except getopt.GetoptError as err:
    print(err)
    usage()

for opt, arg in options:
    if opt in ('-h', '--help'):
        help = True
    elif opt in ('-f', '--file'):
        file = arg
    elif opt in ('-a', '--abbrev'):
        abbrev = arg
    elif opt in ('-u', '--users'):
        users = arg

## Sanity check
if help is True:
    usage()
if file == '':
    print('ERROR: Must provide the password file')
    usage()
if abbrev == '':
    print('ERROR: Must provide the customer abbreviation')
    usage()
if users == '':
    print('ERROR: Must provide the listing of users')
    usage()

safe = '%s-Linux_Server' % abbrev
users = re.split(',', users)

with open(file) as f:
    print('Password_name,Safe,Folder,Password,CI_Name,UserName,CustomerAbbr,DeviceType,PolicyID,Address,ObjectName,LogonDomain,Port')
    for line in f:
        s = re.split(' ', line.rstrip('\n'))
        if s[0] != '' and s[1] in users and s[2] != '':
            server = s[0]
            user = s[1]
            password = s[2]

            password_name = '%s-%s_%s' % (abbrev,server.upper(),s[1])
            ci_name = '%s-%s' % (abbrev,server.upper())

            print('%s,%s,root,"%s",%s,%s,%s,,,,%s,,' % (password_name,safe,password,ci_name,user,abbrev,password_name))

