#!/usr/bin/env python

import os
import re
import sys
import getopt
import json
from decimal import *
#from decimal import Decimal
from pprint import pprint
import csv


###########################
## Define some variables ##
###########################

self = os.path.basename(sys.argv[0])
uid = os.geteuid()

dir = ''
output = ''
help = False

def usage():
   print('\nUsage: %s [OPTION]... [OPTION]...' % self)
   print """
       --dir
              specify the top level directory of the ansible collected data

       --output
              specify the csv file to write

       --help
              display this help menu
"""
   sys.exit(2)

try:
   options, remainder = getopt.gnu_getopt(sys.argv[1:], 'hd:o:', ['help', 'dir=', 'output='])
except getopt.GetoptError as err:
   print(err)
   usage()

for opt, arg in options:
    if opt in ('-h', '--help'):
        help = True
    elif opt in ('-d', '--dir'):
        dir = arg
    elif opt in ('-o', '--output'):
        output = arg

##################
## Sanity check ##
##################

if help is True or len(options) == 0:
   usage()
elif dir == '':
   print "ERROR: Must specify the top level directory of the ansible collected data is"
   usage()
elif output == '':
   print "ERROR: Must specify the name of the csv file to create"
   usage()

if os.path.isdir(dir) is False:
   print('ERROR: the dir %s does not exist... exiting.' % dir)
   sys.exit(2)

if os.path.isfile(output) is True:
   print('ERROR: the file %s already exist... exiting.' % output)
   sys.exit(2)

## Get list of directories in dir/output directory
found = os.listdir("%s/output" % dir)

## If dir/output/server/setup file exists
servers = []
skipped = []
for srv in sorted(found):
   if os.path.isfile("%s/output/%s/setup.json" % (dir,srv)):
      servers.append(srv)
   else:
      skipped.append(srv)

alldata = {}
for server in servers:
   #print('==> %s <==' % server)
   print server
   alldata[server] = {}
   alldata[server]['hostname'] = server

   outputs = '%s/output/%s' % (dir,server)
   files = '%s/fetched/%s' % (dir,server)

   ############
   ## GATHER ##
   ############

   ## iptables_rules
   #alldata[server]['iptables_loaded'] = 'no'
   #if os.path.isfile('%s/iptables_rules' % outputs) and os.stat('%s/iptables_rules' % outputs).st_size != 0:
   #   alldata[server]['iptables_loaded'] = 'yes'

   ## Ansible setup
   with open('%s/setup.json' % outputs) as data_file:
      data = json.load(data_file)
      #print json.dumps(data, sort_keys=True, indent=4)

      # System
      alldata[server]['kernel'] = data['ansible_kernel']
      alldata[server]['architecture'] = data['ansible_architecture']
      #alldata[server]['os'] = data['ansible_lsb']['description']
      alldata[server]['os'] = data['ansible_distribution']
      #alldata[server]['version'] = data['ansible_lsb']['release']
      alldata[server]['version'] = data['ansible_distribution_version']
      alldata[server]['family'] = data['ansible_os_family']
      alldata[server]['model'] = data['ansible_product_name']
      alldata[server]['serial'] = data['ansible_product_serial']
      alldata[server]['vendor'] = data['ansible_system_vendor']
      alldata[server]['selinux'] = data['ansible_selinux']['mode']

      # Network
      alldata[server]['ip'] = data['ansible_default_ipv4']['address']
      alldata[server]['netmask'] = data['ansible_default_ipv4']['netmask']
      alldata[server]['interface'] = data['ansible_default_ipv4']['interface']
      alldata[server]['gateway'] = data['ansible_default_ipv4']['gateway']
      alldata[server]['macaddress'] = data['ansible_default_ipv4']['macaddress']

      # Resources
      alldata[server]['memtotal'] = data['ansible_memtotal_mb']
      alldata[server]['memfree'] = data['ansible_memfree_mb']
      alldata[server]['swaptotal'] = data['ansible_swaptotal_mb']
      alldata[server]['swapfree'] = data['ansible_swapfree_mb']
      alldata[server]['cores'] = data['ansible_processor_cores']
      alldata[server]['processors'] = data['ansible_processor_count']
      alldata[server]['threads'] = data['ansible_processor_threads_per_core']
      alldata[server]['vcpus'] = data['ansible_processor_vcpus']

      # Disk
      space = []
      for disk in data['ansible_mounts']:
         mountpoint = disk['mount']
         try:
            #used = Decimal(((Decimal(disk['size_total']) - Decimal(disk['size_available'])) / disk['size_total']) * 100).quantize(Decimal('.01'), rounding=ROUND_UP)
            used = Decimal(((Decimal(disk['size_total']) - Decimal(disk['size_available'])) / disk['size_total']) * 100).quantize(Decimal('1'), rounding=ROUND_UP)
         except InvalidOperation:
            used = 0
         if used >= 90:
            space.append("%s (%s%%)" % (mountpoint, used))

      if len(space) >= 1:
         alldata[server]['spacealert'] =''
         for i in xrange(0, len(space)):
            if i < (len(space)-1):
               alldata[server]['spacealert'] += "%s\015" % space[i]
            else:
               alldata[server]['spacealert'] += space[i]

      #print alldata[server]['spacealert']

   ############
   ## REPORT ##
   ############

   #print os
   #for fs in space:
   #   print fs

if len(skipped) >= 1:
   print
   print "WARNING: skipped the following servers because 'setup' file missing"
   for server in skipped:
      print server

###############
## Write CSV ##
###############

csv_columns = ['hostname','architecture','os','version','family','kernel','ip','netmask','gateway','interface','macaddress','model','serial','vendor','selinux','memtotal','memfree','swaptotal','swapfree','cores','processors','threads','vcpus','spacealert']
try:
   with open("%s" % output, "wb") as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_columns, quoting=csv.QUOTE_NONNUMERIC, dialect='excel')
      #writer.writeheader() #not supported in this version of python
      writer.writerow(dict(zip(writer.fieldnames, writer.fieldnames)))
      for server in alldata:
         writer.writerow(alldata[server])
except IOError as (errno, strerror):
   print("I/O error({0}): {1}" . format(errno, strerror))
csvfile.close()

print
print "Wrote %s" % output
print "Have a nice day!"

sys.exit(0)

#grep 'alldata\[server\]\[' linux_report.py | cut -d\' -f2 | xargs | sed -e "s/^/\'/g;s/$/\'/g;s/ /\',\'/g"
