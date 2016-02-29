#!/bin/bash

touch -t $(date --date='yesterday 00:00' '+%y%m%d%H%M.%S') /var/spool/cron/lastrun/cron.daily
sed -i '/\/var\/log\/firepower/d' /var/lib/logrotate.status
