#!/usr/bin/env python

import os
import re
import sys
import getopt

self = os.path.basename(sys.argv[0])

file = ''
outdir = ''
user = ''
help = False

def usage():
    print('\nUsage: %s [OPTION]... [OPTION]...' % self)
    print """
       --file
              file that has password information
              #server user clear_text_pass password_hash

       --outdir
              directory to create the files in

       --user
              non-root user to ssh into remote systems

       --help
              display this help menu
"""
    sys.exit(2)

try:
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hf:o:u:', ['help', 'file=', 'outdir=', 'user='])
except getopt.GetoptError as err:
    print(err)
    usage()

for opt, arg in options:
    if opt in ('-h', '--help'):
        help = True
    elif opt in ('-f', '--file'):
        file = arg
    elif opt in ('-o', '--outdir'):
        outdir = arg
    elif opt in ('-u', '--user'):
        user = arg

## Sanity check
if help is True:
    usage()
if file == '':
    print('ERROR: Must provide the password file')
    usage()
if outdir == '':
    print('ERROR: Must provide the output directory')
    usage()
if user == '':
    print('ERROR: Must provide the non-root user')
    usage()

if not os.path.exists(outdir):
    print('ERROR: %s does not exist' % outdir)
    sys.exit(1)

data = {}
with open(file) as f:
    for line in f:
        s = re.split(' ', line.rstrip('\n'))
        if s[0] != '' and s[1] == user and s[2] != '':
            server = s[0]
            user = s[1]
            password = s[2]

            try:
                fd = os.open('%s/%s.yml' % (outdir,server), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o0600)
                f = os.fdopen(fd, "wb")
                f.write('---\n\n')
                f.write('ansible_user: %s\n' % user)
                f.write('ansible_ssh_pass: \'%s\'\n' % password)
                f.write('ansible_sudo_pass: \'%s\'\n' % password)
                f.write('\n')
            except:
                print('ERROR: unable to open %s/%s' % (outdir,server))
                sys.exit(1)
            f.close

