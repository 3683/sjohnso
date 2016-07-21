#!/bin/bash

SELF=$(basename $0)

usage() {
   cat << USAGE
Usage: ${SELF} [OPTION]... [OPTION]...

Options:
  -h|--help             show this help message and exit
  -k|--key KEY          name of the RSA private key to create
                        (e.g. id_rsa_mykey)
USAGE
   exit 1
}

error() {
   echo "ERROR: $1"
   exit 1
}

if [[ ! "$@" ]] ; then
   usage
fi

getopt -T > /dev/null
if [ $? -eq 4 ]; then
   # GNU enhanced getopt is available
   eval set -- `getopt -o hk: -l help,key: -n ${SELF} -- "$@"`
else
   # Original getopt is available
   set -- `getopt hk: "$@"`
fi

while true ; do
   case "$1" in
      -k|--key)
         KEY=$2; shift;;
      -h|--help)
         usage;;
      --)
         shift; break;;
      *)
         usage;;
   esac
   shift
done

if [ "${KEY}" = "" ] ; then
   error "must specify the private RSA key to create... exiting."
fi

ssh-keygen -t rsa -N "" -f ${KEY}

