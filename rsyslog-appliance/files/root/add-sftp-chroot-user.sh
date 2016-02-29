#!/bin/bash

SFTPGROUP=sftpusers
JAILDIR=/var/log/url
SSHDCONFIG=/etc/ssh/sshd_config
SELF=$(basename $0)

if [ ! $1 ] ; then
   echo "Usage: ${SELF} [user]"
   exit 1
fi

ADDUSER=$1

##
## Check for OS user
##

if `awk -F: '{print $1}' /etc/passwd | grep -q ${ADDUSER}` ; then
   echo "ERROR: ${ADDUSER} already exists"
   exit 1
fi

##
## Check/add OS group
##

if ! `awk -F: '{print $1}' /etc/group | grep -q ${SFTPGROUP}` ; then
   echo "Adding ${SFTPGROUP} group"
   groupadd ${SFTPGROUP}
fi

##
## Add OS user
##

echo "Adding ${ADDUSER} user"
useradd -G ${SFTPGROUP} -M ${ADDUSER}
mkdir /home/${ADDUSER}
chmod 0700 /home/${ADDUSER}
chown -R ${ADDUSER}:users /home/${ADDUSER}

##
## Check/change sftp-server to internal-sftp
##

SSHRELOAD=no
if `egrep -v "^(#|$)" ${SSHDCONFIG} | grep -iq /usr/lib64/ssh/sftp-server` ; then
   echo "Changing SSHD sftp subsystem to internal-sftp"
   sed -i '/\/usr\/lib64\/ssh\/sftp-server/s/^/#/g' ${SSHDCONFIG}
   sed -i '/\/usr\/lib64\/ssh\/sftp-server/a Subsystem'"\t"'sftp'"\t"'internal-sftp' ${SSHDCONFIG}
   SSHRELOAD=yes
fi

##
## Check for AllowGroups membership
##

if ! `egrep -v "^(#|$)" ${SSHDCONFIG} | grep -i "^AllowGroups" | grep -iq "${SFTPGROUP}"` ; then
   echo "Adding ${SFTPGROUP} to AllowGroups"
   if `grep -iq "^AllowGroups" ${SSHDCONFIG}` ; then
      echo "Append to AllowGroups"
      sed -i "s/^\(AllowGroups.*\)/\1 ${SFTPGROUP}/g" ${SSHDCONFIG}
   else
      echo "Adding AllowGroups"
      echo "AllowGroups ${SFTPGROUP}" >> ${SSHDCONFIG}
   fi
   SSHRELOAD=yes
fi

##
## Check/add Match group
##

if ! `egrep -v "^(#|$)" ${SSHDCONFIG} | grep -iq "Match Group ${SFTPGROUP}"` ; then
   echo "Adding SSHD Match Group ${SFTPGROUP} stansa"
   TAB=$'\t'
   cat << EOM >> ${SSHDCONFIG}

Match Group ${SFTPGROUP}
${TAB}X11Forwarding no
${TAB}AllowTcpForwarding no
${TAB}ChrootDirectory ${JAILDIR}
${TAB}ForceCommand internal-sftp

EOM
   SSHRELOAD=yes
fi

##
## Restart sshd if needed
##

if [ "${SSHRELOAD}" = "yes" ] ; then
   service sshd restart
fi
