#!/bin/bash

if [ ! -e "/.done" ] ; then
   touch /.done
   rm -f /etc/ssh/ssh_*_key > /dev/null 2>&1
   echo "Creating host SSH keys"
   ssh-keygen -A

   EXISTING=$(awk -F: -v groupid=${GROUPID} '$3 == groupid {print $1}' /etc/group)
   if [ "${EXISTING}" != "" ] ; then
      delgroup ${EXISTING}
   fi

   addgroup -g ${GROUPID} ${GROUP}
   adduser -h /home/${USER} -s /bin/bash -u ${USERID} -G ${GROUP} -D ${USER}
   passwd -u ${USER}

   chown ${USERID}:${GROUPID} /a
fi

if [ "${AUTHORIZED_KEYS}" != "**None**" ]; then
   echo "=> Found authorized keys"
   mkdir -p /home/${USER}/.ssh
   chmod 700 /home/${USER}/.ssh
   touch /home/${USER}/.ssh/authorized_keys
   chmod 600 /home/${USER}/.ssh/authorized_keys
   IFS=$'\n'
   arr=$(echo ${AUTHORIZED_KEYS} | tr "," "\n")
   for x in $arr ; do
      x=$(echo $x |sed -e 's/^ *//' -e 's/ *$//')
      cat /home/${USER}/.ssh/authorized_keys | grep "$x" >/dev/null 2>&1
      if [ $? -ne 0 ]; then
         echo "=> Adding public key to /home/${USER}/.ssh/authorized_keys: $x"
         echo "$x" >> /home/${USER}/.ssh/authorized_keys
      fi
   done
   chown -R ${USERID}:${GROUPID} /home/${USER}/.ssh
fi

if [ "${AUTHORIZED_KEYS}" != "**None**" ]; then
   echo "=> Found authorized keys"
   mkdir -p /root/.ssh
   chmod 700 /root/.ssh
   touch /root/.ssh/authorized_keys
   chmod 600 /root/.ssh/authorized_keys
   IFS=$'\n'
   arr=$(echo ${AUTHORIZED_KEYS} | tr "," "\n")
   for x in $arr ; do
      x=$(echo $x |sed -e 's/^ *//' -e 's/ *$//')
      cat /root/.ssh/authorized_keys | grep "$x" >/dev/null 2>&1
      if [ $? -ne 0 ]; then
         echo "=> Adding public key to /root/.ssh/authorized_keys: $x"
         echo "$x" >> /root/.ssh/authorized_keys
      fi
   done
fi

exec /usr/sbin/sshd -D
