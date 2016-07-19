#!/bin/bash

SELF=$(basename $0)

usage() {
   cat << USAGE
Usage: ${SELF} [OPTION]... [OPTION]...

Options:
  -h|--help             show this help message and exit
  -k|--key KEY          private RSA ssh key that will be used
                        to connect to container
  -n|--name NAME        name of the container to create
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
   set -- `getopt -o hk:n: -l help,key:,name: -n ${SELF} -- "$@"`
else
   # Original getopt is available
   set -- `getopt hk:n: "$@"`
fi

while true ; do
   case "$1" in
      -k|--key)
         KEY=$2; shift;;
      -n|--name)
         NAME=$2; shift;;
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
   error "must specify the private RSA key used to connect to container... exiting."
fi
if [ "${NAME}" = "" ] ; then
   error "must specify the name of the container to create... exiting."
fi
if [ ! -e "${KEY}" ] ; then
   error "${KEY} does not exist... exiting."
elif [ ! -f "${KEY}" ] ; then
   error "${KEY} is not a file... exiting."
fi

PORT=$(docker port ${NAME} 22/tcp | cut -d: -f2)

exec ssh -x -p ${PORT} -o "UserKnownHostsFile /dev/null" -o "StrictHostKeyChecking no" -i ${KEY} ${USER}@localhost

