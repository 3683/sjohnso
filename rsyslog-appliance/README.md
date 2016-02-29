#### Put files into place

```sh
cp -p files/etc/logrotate.d/firepower /etc/logrotate.d

mv /etc/rsyslog.conf /etc/rsyslog.conf.bak
cp -p files/etc/rsyslog.conf /etc

cp -p files/etc/rsyslog.d/1-remote.conf /etc/rsyslog.d
cp -p files/etc/rsyslog.d/2-firepower.conf /etc/rsyslog.d
cp -p files/etc/rsyslog.d/3-bmn.conf /etc/rsyslog.d

mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
cp -p files/etc/ssh/sshd_config /etc/ssh
chmod 0640 /etc/ssh/sshd_config

mv /etc/sysconfig/cron /etc/sysconfig/cron.bak
cp -p files/etc/sysconfig/cron /etc/sysconfig

mv /etc/sysconfig/scripts/SuSEfirewall2-custom /etc/sysconfig/scripts/SuSEfirewall2-custom.bak
cp -p files/etc/sysconfig/scripts/SuSEfirewall2-custom /etc/sysconfig/scripts
chmod 0755 /etc/sysconfig/scripts/SuSEfirewall2-custom

mv /etc/sysconfig/syslog /etc/sysconfig/syslog.bak
cp -p files/etc/sysconfig/syslog /etc/sysconfig

mv /etc/sysconfig/SuSEfirewall2 /etc/sysconfig/SuSEfirewall2.bak
cp -p files/etc/sysconfig/SuSEfirewall2 /etc/sysconfig

cp -p files/root/add-sftp-chroot-user.sh /root
cp -p files/root/create-log-dirs.sh /root
cp -p files/root/set-cron-daily.sh /root
chmod +x /root/{add-sftp-chroot-user.sh,create-log-dirs.sh,set-cron-daily.sh}
```

#### Update hosts file with IP/name

Update /etc/hosts so that each appliance IP and its name are present:

```sh
10.60.0.9       appliance1
10.60.0.10      appliance2
10.60.0.17      appliance3
```

#### Setup log directories

```sh
/root/create-log-dirs.sh
```

#### Restart some things

```sh
service syslog restart
service sshd restart
/sbin/SuSEfirewall2
```

#### Add a local user account to have sftp-only access to the /var/log/firepower directory

```sh
/root/add-sftp-chroot-user.sh user1
```
