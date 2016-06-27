#!/usr/bin/env python

import os
import re
import sys
import yaml
import json
import subprocess

file = 'dyn.yml'

with open(file) as data_file:
    data = yaml.load(data_file)

#print yaml.dump(data, default_flow_style=False)
#print json.dumps(data, indent=2, sort_keys=True)

def gen_password(file, server, user):
    p = subprocess.Popen(['/a/bin/genpasshash.py', '-s', server, '-u', user, '-f', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return p.returncode, stdout, stderr

def get_hash(file, server, user):
    hash = ''
    try:
        # get hash if it already exists
        with open(file) as f:
            for line in f:
                s = re.split(' ', line.rstrip('\n'))
                if s[0] == server and s[1] == user and s[3] != '':
                    hash = s[3]
                    continue
    except:
        pass

    if hash == '':
        # password/hash needs to be generated
        result = gen_password(file, server, user)
        if result[1] != '':
            hash = result[1]
    if hash == '':
        hash = 'this_hash_is_invalid'
    return hash

for server in data['_meta']['hostvars']:
    try:
        data['_meta']['hostvars'][server]['users']
    except:
        continue
    for idx, val in enumerate(data['_meta']['hostvars'][server]['users']):
        user = data['_meta']['hostvars'][server]['users'][idx]['name']

        hash = get_hash(data['_meta']['hostvars']['all']['passfile'], server, user)
        data['_meta']['hostvars'][server]['users'][idx]['hash'] = hash

if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    print data
    #print json.dumps(data, indent=2)
elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
    #print data['_meta']['hostvars'][sys.argv[2]]
    print json.dumps(data['_meta']['hostvars'][sys.argv[2]], indent=2, sort_keys=True)
else:
    print "Usage: %s --list or --host <hostname>" % sys.argv[0]
    sys.exit(1)

