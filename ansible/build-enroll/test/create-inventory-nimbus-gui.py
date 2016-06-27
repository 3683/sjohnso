#!/usr/bin/env python

import os
import re
import sys
import getopt
import csv

###########################
## Define some variables ##
###########################

self = os.path.basename(sys.argv[0])
uid = os.geteuid()

file = ''
output = ''
help = False

def usage():
   print('\nUsage: %s [OPTION]... [OPTION]...' % self)
   print """
       --file
              specify the file that contains lines: bmn,ci,ip

       --output
              specify the inventory output file to create

       --help
              display this help menu
"""
   sys.exit(2)

try:
   options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hf:o:', ['help', 'file=', 'output='])
except getopt.GetoptError as err:
   print(err)
   usage()

for opt, arg in options:
    if opt in ('-h', '--help'):
        help = True
    elif opt in ('-f', '--file'):
        file = arg
    elif opt in ('-o', '--output'):
        output = arg

##################
## Sanity check ##
##################

if help is True or len(options) == 0:
   usage()
elif file == '':
   print "ERROR: Must specify the file containing bmn,ci,ip"
   usage()
elif output == '':
   print "ERROR: Must specify the invenroty output file to create"
   usage()

if os.path.isfile(file) is False:
   print('ERROR: the file %s does not exist... exiting.' % file)
   sys.exit(2)

if os.path.isfile(output) is True:
   print('ERROR: the file %s already exist... exiting.' % output)
   sys.exit(2)

if os.stat(file).st_size == 0:
   print('ERROR: the file %s is empty... exiting.' % file)

##############
## Get data ##
##############

## Get hostname of this BMN
thishostname = os.uname()[1]

## Read in /etc/hosts
etchosts = []
with open('/etc/hosts') as data_file:
   for line in data_file:
      m = re.search("^\d", line.rstrip())
      if m:
         etchosts.append(line.rstrip())

## Read in tab delimited output from NimBUS Manager GUI
hosts = {}
try:
   with open(file, "r") as csvfile:
      reader = csv.reader(csvfile, delimiter='\t')
      cnt = 0
      header = []
      server = ''
      for line in reader:
         cnt += 1
         if cnt == 1:
            header = line
            continue
         server = line[0]
         hosts[server] = {}
         for i in xrange(0, len(header)):
            hosts[server][header[i]] = line[i]

except IOError as (errno, strerror):
   print("I/O error({0}): {1}" . format(errno, strerror))
csvfile.close()

## Verify ci/ip match /etc/hosts entry
good = []
bmn = re.compile('^[a-zA-Z]+-s-[rb]mn\d+')
for server in sorted(hosts):
   # Skip BMN
   if bmn.match(server):
      continue
   # Skip non-Linux
   if hosts[server]['OS Minor'] != 'Linux':
      continue
   # Skip CIs that are not on this BMN
   nimaddress = hosts[server]['Address'].split('/')
   if nimaddress[2] != thishostname:
      print('WARNING: the CI %s is no accessible via this BMN... skipping.' % server)
      continue
   # Skip CIs where the server doesn't match the robot name
   if nimaddress[3] != server:
      print('WARNING: %s has a CI/Robot mis-match... skipping.' % server)
      continue
   found = False
   for line in etchosts:
      if found:
         continue
      split = line.split()
      for i in xrange(1, len(split)):
         if split[i] == server:
            found = True
            if split[0] != hosts[server]['IP']:
               print('WARNING: the IP for %s does not match (should be %s)... skipping.') % (server, hosts[server]['IP'])
            else:
               print server
               good.append(server)
   if not found:
      print('WARNING: the CI name %s was not found in /etc/hosts... skipping.' % hosts[server]['Robot'])

## Verify we still have good servers to deal with
if len(good) < 1:
   print('ERROR: no servers left after verification... exiting.')
   sys.exit(1)

## Write the inventory file
try:
   f = open(output, 'w')
except IOError as (errno, strerror):
   print("I/O error({0}): {1}" . format(errno, strerror))

for server in sorted(good):
   f.write("%s\n" % server)

f.close()

print
print "Wrote inventory file %s" % output
print
print "Execute the following command to verify the setup:"
print "     ansible all -i %s -u <user> --ask-pass -m ping" % output
print
print "Have a nice day!"

sys.exit(0)
