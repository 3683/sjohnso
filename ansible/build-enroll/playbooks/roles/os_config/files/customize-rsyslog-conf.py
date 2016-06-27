#!/usr/bin/env python

import os
import re
import sys
import subprocess

file_in = '/etc/rsyslog.conf'
file_out = '/etc/rsyslog.conf.new'

def chcon(src, dst):
    bin = '/usr/bin/chcon'
    if os.path.isfile(bin) and os.access(bin, os.X_OK):
        p = subprocess.Popen([bin, "--reference", src, dst], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = p.communicate()
        return p.returncode, stdout, stderr

try:
    o = open(file_out, 'w')
except:
    print('ERROR: Unable to %s' % file_out)
    sys.exit(1)

with open(file_in) as f:
    for line in f:
        if not re.match("(#|$)", line):
            blah = re.split("\s*", line)
            if re.search("\.", blah[0]):
                if not re.search("^\*$", blah[1]):
                    line = re.sub(r'^', '#', line)
        o.write(line)

f.close()
o.close()

chcon(file_in, file_out)

try:
    os.rename(file_out, file_in)
except:
    print('ERROR: Unable to move %s to %s' % (file_out, file_in))
    sys.exit(1)

sys.exit(0)
