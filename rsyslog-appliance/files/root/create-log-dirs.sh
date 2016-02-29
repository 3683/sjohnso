#!/bin/bash

groupadd firepower
mkdir -p /var/log/firepower/archive
chown -R root:firepower /var/log/firepower
chmod -R 0750 /var/log/firepower
