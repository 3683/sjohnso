#!/bin/bash

HOSTS=./dyn.py
OUTPUT=$(pwd)/qa-$(date +'%Y-%m-%d')

ansible-playbook \
-v \
-i ${HOSTS} \
--ask-vault-pass \
-e "outputdir=${OUTPUT}" \
playbooks/qa.yml

