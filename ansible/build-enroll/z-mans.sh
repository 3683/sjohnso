#!/bin/bash

HOSTS=./dyn.py

#ansible internal -i ${HOSTS} -u root --ask-pass -m shell -a uptime
#ansible internal -i ${HOSTS} -u root --ask-pass -m shell -a "shutdown -h now"

# OS config
ansible-playbook \
-v \
-i ${HOSTS} \
-u root \
--ask-pass \
-e ansible_pub_ssh_key=$(pwd)/keys/id_dsa_ansible.pub \
-e genpasshashpy=$(pwd)/bin/genpasshash.py \
-e passfile=passfile \
-e setpass=true \
playbooks/mans.yml

