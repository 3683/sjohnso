#!/usr/bin/env python

import os
import platform
import re
import stat
import sys
import select
import shlex
import subprocess

osplatform = platform.system()

def run_cmd(cmd, live=True, readsize=10):
    cmdargs = shlex.split(cmd)
    p = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout = ''
    stderr = ''
    rpipes = [p.stdout, p.stderr]
    while True:
        rfd, wfd, efd = select.select(rpipes, [], rpipes, 1)

        if p.stdout in rfd:
            dat = os.read(p.stdout.fileno(), readsize)
            if live:
                sys.stdout.write(dat)
            stdout += dat
            if dat == '':
                rpipes.remove(p.stdout)
        if p.stderr in rfd:
            dat = os.read(p.stderr.fileno(), readsize)
            stderr += dat
            if live:
                sys.stdout.write(dat)
            if dat == '':
                rpipes.remove(p.stderr)
        # only break out if we've emptied the pipes, or there is nothing to
        # read from and the process has finished.
        if (not rpipes or not rfd) and p.poll() is not None:
            break
        # Calling wait while there are still pipes to read can cause a lock
        elif not rpipes and p.poll() == None:
            p.wait()

    return p.returncode, stdout, stderr

def get_file_content(path, default=None, strip=True):
    data = default
    if os.path.exists(path) and os.access(path, os.R_OK):
        try:
            try:
                datafile = open(path)
                data = datafile.read()
                if strip:
                    data = data.strip()
                if len(data) == 0:
                    data = default
            finally:
                datafile.close()
        except:
            # ignore errors as some jails/containers might have readable permissions but not allow reads to proc
            # done in 2 blocks for 2.4 compat
            pass
    return data

def get_file_lines(path):
    '''get list of lines from file'''
    data = get_file_content(path)
    if data:
        ret = data.splitlines()
    else:
        ret = []
    return ret

def is_executable(path):
    '''is the given path executable?'''
    return (stat.S_IXUSR & os.stat(path)[stat.ST_MODE]
            or stat.S_IXGRP & os.stat(path)[stat.ST_MODE]
            or stat.S_IXOTH & os.stat(path)[stat.ST_MODE])

def get_bin_path(arg, required=False, opt_dirs=[]):
    '''
    find system executable in PATH.
    Optional arguments:
       - required:  if executable is not found and required is true, fail_json
       - opt_dirs:  optional list of directories to search in addition to PATH
    if found return full path; otherwise return None
    '''
    sbin_paths = ['/sbin', '/usr/sbin', '/usr/local/sbin']
    paths = []
    for d in opt_dirs:
        if d is not None and os.path.exists(d):
            paths.append(d)
    paths += os.environ.get('PATH', '').split(os.pathsep)
    bin_path = None
    # mangle PATH to include /sbin dirs
    for p in sbin_paths:
        if p not in paths and os.path.exists(p):
            paths.append(p)
    for d in paths:
        path = os.path.join(d, arg)
        if os.path.exists(path) and is_executable(path):
            bin_path = path
            break
    if required and bin_path is None:
        self.fail_json(msg='Failed to find required executable %s' % arg)
    return bin_path

def get_distribution():
    ''' return the distribution name '''
    if osplatform == 'Linux':
        try:
            supported_dists = platform._supported_dists + ('arch',)
            distribution = platform.linux_distribution(supported_dists=supported_dists, full_distribution_name=0)[0].capitalize()
            if not distribution and os.path.isfile('/etc/system-release'):
                distribution = platform.linux_distribution(supported_dists=['system'], full_distribution_name=0)[0].capitalize()
                if 'Amazon' in distribution:
                    distribution = 'Amazon'
                else:
                    distribution = 'OtherLinux'
        except:
            # FIXME: MethodMissing, I assume?
            distribution = platform.dist()[0].capitalize()
    elif osplatform == 'AIX':
        distribution = osplatform
    else:
        distribution = None
    return distribution

def get_distribution_version():
    ''' return the distribution version '''
    if osplatform == 'Linux':
        try:
            distribution_version = platform.linux_distribution()[1]
            if not distribution_version and os.path.isfile('/etc/system-release'):
                distribution_version = platform.linux_distribution(supported_dists=['system'])[1]
        except:
            # FIXME: MethodMissing, I assume?
            distribution_version = platform.dist()[1]
    elif osplatform == 'AIX':
        distribution_version = '%s.%s' % (platform.version(), platform.release())
    else:
        distribution_version = None
    return distribution_version

def get_lsbrelease():
    ''' return the distribution version using lsb_release '''
    lsbinfo = None
    distro_id = ''
    distro_release = ''
    lsb_path = get_bin_path('lsb_release')
    if lsb_path:
        rc, out, err = run_cmd('%s -a' % lsb_path, live=False)
        if rc == 0:
            for line in out.split('\n'):
                if len(line) < 1 or ':' not in line:
                    continue
                value = line.split(':', 1)[1].strip()
                if 'Distributor ID:' in line:
                    value = re.sub(r'SUSE LINUX', r'suse', value, re.I)
                    value = re.sub(r'RedHatEnterpriseServer', r'redhat', value, re.I)
                    distro_id = value.title()
                elif 'Release:' in line:
                    distro_release = value
    elif lsb_path is None and os.path.exists('/etc/lsb-release'):
        for line in get_file_lines('/etc/lsb-release'):
            value = line.split('=',1)[1].strip()
            if 'DISTRIB_ID' in line:
                distro_id = value.title()
            elif 'DISTRIB_RELEASE' in line:
                distro_release = value
    if distro_id != '' and distro_release != '':
        lsbinfo = '%s %s' % (distro_id, distro_release)
    return lsbinfo

def main():
    if osplatform == 'Linux' and sys.version_info[0] < 3 and sys.version_info[1] < 6:
        cdw_os = '%s %s' % (get_lsbrelease(), platform.architecture()[0])
    else:
        cdw_os = '%s %s %s' % (get_distribution(), get_distribution_version(), platform.architecture()[0])
    print('cdw_os %s' % cdw_os)

if __name__ == '__main__':
    main()

