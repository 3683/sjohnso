#!/bin/bash

SELF=$(basename $0)

usage() {
   cat << USAGE
Usage: ${SELF} [OPTION]... [OPTION]...

Options:
  -h|--help             show this help message and exit
  -p|--port PORT        The TCP port that will forward to
                        22/tcp of the container
  -k|--key KEY          private RSA ssh key that will be used
                        to connect to container
  -i|--image IMAGE      docker image to create container
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
   eval set -- `getopt -o hp:k:i:n: -l help,port:,key:,image:,name: -n ${SELF} -- "$@"`
else
   # Original getopt is available
   set -- `getopt hp:k:i:n: "$@"`
fi

while true ; do
   case "$1" in
      -p|--port)
         PORT=$2; shift;;
      -k|--key)
         KEY=$2; shift;;
      -i|--image)
         IMAGE=$2; shift;;
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

if [ "${PORT}" = "" ] ; then
   error "must specify tcp port that will forward to 22/tcp of container... exiting."
fi
if [ "${KEY}" = "" ] ; then
   error "must specify the private RSA key used to connect to container... exiting."
fi
if [ "${IMAGE}" = "" ] ; then
   error "must specify the docker image to create the container from... exiting."
fi
if [ "${NAME}" = "" ] ; then
   error "must specify the name of the container to create... exiting."
fi

GROUP=$(groups ${USER} | awk '{print $1}')
USERID=$(id -u)
GROUPID=$(id -g)
PUB=$(cat ${KEY}.pub)

if [ "${GROUP}" = "" ] ; then
   error "unable to determine the primary group of the ${USER} user... exiting."
fi
if [ "${USERID}" = "" ] ; then
   error "unable to determine the user ID of the ${USER} user... exiting."
fi
if [ "${GROUPID}" = "" ] ; then
   error "unable to determine the group ID of the ${USER} user... exiting."
fi
if [ "${PUB}" = "" ] ; then
   error "unable to get the public key from ${KEY}.pub... exiting."
fi

docker run -d \
-p ${PORT}:22 \
-e AUTHORIZED_KEYS="${PUB}" \
-e USER=${USER} \
-e GROUP=${GROUP} \
-e USERID=${USERID} \
-e GROUPID=${GROUPID} \
--hostname ${NAME} \
--name ${NAME} \
-v $HOME:/a \
${IMAGE}

