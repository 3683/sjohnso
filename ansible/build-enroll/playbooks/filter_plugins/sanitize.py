#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

def fixme(a):
    omit = [ 'ansible_ssh_pass', 'ansible_su_pass', 'ansible_sudo_pass', 'rhn_pass', 'snmpd_password' ]
    fixed = {}
    for key in sorted(a):
        if key not in omit:
            fixed[key] = a[key]
    return fixed

class FilterModule(object):
    ''' Ansible fixme jinja2 filters '''

    def filters(self):
        return {
            'fixme': fixme,

        }
