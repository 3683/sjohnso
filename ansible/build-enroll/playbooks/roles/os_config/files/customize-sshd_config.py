#!/usr/bin/env python

import os
import re
import sys
import subprocess

file_in = '/etc/ssh/sshd_config'
file_out = '/etc/ssh/sshd_config.new'

try:
    o = open(file_out, 'w')
except:
    print('ERROR: Unable to %s' % file_out)
    sys.exit(1)

wants = {
  'Protocol': '2',
  'PermitRootLogin': 'yes',
  'TCPKeepAlive': 'yes',
  'ClientAliveInterval': '15'
}

def copy_perm(src, dst):
    user = os.stat(src).st_uid
    group = os.stat(src).st_gid
    mode = os.stat(src).st_mode
    os.chmod(dst, mode)
    os.chown(dst, user, group)

def chcon(src, dst):
    bin = '/usr/bin/chcon'
    if os.path.isfile(bin) and os.access(bin, os.X_OK):
        p = subprocess.Popen([bin, "--reference", src, dst], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        return p.returncode, stdout, stderr

def check_set(array, parameter):
    new = []
    #print('==> checking for %s <==' % parameter)
    found = 0
    for line in array:
        content = ''
        if re.search('^%s' % parameter, line):
            #print('Found %s: %s' % (parameter, line))
            found = 1
            m = re.match('^%s [ ]*(.*)' % parameter, line)
            if m:
                if m.group(1) == wants[parameter]:
                    #print('DEBUG: no action is needed')
                    new.append(line)
                else:
                    #print('DEBUG: changing uncommented line to %s %s' % (parameter, wants[parameter]))
                    new.append('%s %s' % (parameter, wants[parameter]))
        elif re.search('^#[ ]*%s' % parameter, line):
            found = 1
            #print('DEBUG: changing commented line to %s %s' % (parameter, wants[parameter]))
            new.append('%s %s' % (parameter, wants[parameter]))
        else:
            new.append(line)
    if found == 0:
        #print('DEBUG: append line for %s %s' % (parameter, wants[parameter]))
        new.append('%s %s' % (parameter, wants[parameter]))
    return new

content = []
with open(file_in) as f:
    for line in f:
        content.append(line.rstrip('\n'))

for want in wants:
    content = check_set(content, want)

for line in content:
    o.write('%s\n' % line)

f.close()
o.close()

chcon(file_in, file_out)
copy_perm(file_in, file_out)

try:
    os.rename(file_out, file_in)
except:
    print('ERROR: Unable to move %s to %s' % (file_out, file_in))
    sys.exit(1)

sys.exit(0)
