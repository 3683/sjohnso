#!/bin/bash

SELF=$(basename $0)

usage() {
   cat << USAGE
Usage: ${SELF} [OPTION]... [OPTION]...

Options:
  -h|--help             show this help message and exit
  -i|--image IMAGE      name of the image to create
                        (e.g. local/myimage:1.0)
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
   set -- `getopt -o hi: -l help,image: -n ${SELF} -- "$@"`
else
   # Original getopt is available
   set -- `getopt hi: "$@"`
fi

while true ; do
   case "$1" in
      -i|--image)
         IMAGE=$2; shift;;
      -h|--help)
         usage;;
      --)
         shift; break;;
      *)
         usage;;
   esac
   shift
done

if [ "${IMAGE}" = "" ] ; then
   error "must specify the name of the image to create... exiting."
fi

docker build -t ${IMAGE} alpine

