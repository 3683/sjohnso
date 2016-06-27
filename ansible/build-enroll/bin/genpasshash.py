#!/usr/bin/env python

import os
import sys
import getopt
import random
from crypt import crypt
from os import urandom
from random import choice

self = os.path.basename(sys.argv[0])

server = ''
user = ''
file = ''
help = False

def usage():
    print('\nUsage: %s [OPTION]... [OPTION]...' % self)
    print """
       --server
              name of the server this user will be added

       --user
              name of the user for this password

       --file
              path to file to write password to

       --help
              display this help menu
"""
    sys.exit(2)

try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hs:u:f:', ['help', 'server=', 'user=', 'file='])
except getopt.GetoptError as err:
    print(err)
    usage()

for opt, arg in options:
    if opt in ('-h', '--help'):
        help = True
    elif opt in ('-s', '--server'):
        server = arg
    elif opt in ('-u', '--user'):
        user = arg
    elif opt in ('-f', '--file'):
        file = arg

## Sanity check
if help is True:
    usage()
if server == '':
    print('ERROR: Must provide the server name')
    usage()
if user == '':
    print('ERROR: Must provide the user name')
    usage()
if file == '':
    print('ERROR: Must provide the file to write password to')
    usage()

char_set = {'small': 'abcdefghijklmnopqrstuvwxyz',
             'nums': '0123456789',
             'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
             'special': '^!\$%&/()=?{[]}+~#-_.:;<>|'
            }

def generate_pass(length=15):
    """Function to generate a password"""

    password = []

    while len(password) < length:
        key = choice(char_set.keys())
        a_char = urandom(1)
        if a_char in char_set[key]:
            if check_prev_char(password, char_set[key]):
                continue
            else:
                password.append(a_char)
    return ''.join(password)

def check_prev_char(password, current_char_set):
    """Function to ensure that there are no consecutive
    UPPERCASE/lowercase/numbers/special-characters."""

    index = len(password)
    if index == 0:
        return False
    else:
        prev_char = password[index - 1]
        if prev_char in current_char_set:
            return True
        else:
            return False

def eprint(msg):
    print >> sys.stderr, msg

if __name__ == '__main__':
    mypass = generate_pass()
    mysalt = '$6$'
    mysalt += ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(8))
    myhash = crypt(mypass, mysalt)

    try:
        fd = os.open(file, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o0600)
        f = os.fdopen(fd, "wb")
        f.write('%s %s %s %s\n' % (server,user,mypass,myhash))
    except:
        eprint('ERROR: unable to %s' % file)
        sys.exit(1)

    f.close

    print(myhash)

