# Setup docker container

Follow the steps below to stage the docker container and configuration files.  After that is complete, end-point systems should be accessible directly via the docker container for use within Ansible playbooks.

#### 1. Clone 'sjohnso' github.com repository:
```
 git clone https://github.com/cdwlabs/sjohnso.git git/cdw-ansible
 cd git/cdw-ansible
 git filter-branch --prune-empty --subdirectory-filter ansible HEAD
 rm -rf .git
 find . -type f -name ".git*" -exec rm -f {} \;
```

#### 2. Build docker image:
```
 cd proxy
 ./1-build.sh -i local/ansible:0.1
```

#### 3. Create ssh key to connect to docker container
```
 ./2-create-keys.sh -k id_rsa_ansible
```

#### 4. Create the docker container
```
 ./3-run.sh -p 17593 -k id_rsa_ansible -i local/ansible:0.1 -n ansible-1
```

#### 5. Connect to the docker container
```
 ./4-connect.sh -k id_rsa_ansible -n ansible-1
```

# Setup ssh proxies within docker container

#### 1. Create a YAML configuration file that describes which BMN each system connects through:
```
 $ vi hosts-bmn-config.yml
 ---

 dcapps-s-bmn15:
   - h-appsdb-msn-5

 dcapps-s-bmn09:
   - h-appsdb-msp-5

 hcs-s-bmn03:
   - h-hcssftp-ord-3
```

#### 2. Setup the ssh configuration file and .ansible.cfg:
```
 $ create-ssh-config -p h-custmgmt-msn-1.binc.net -c ~/my-ssh-config -f ~/hosts-bmn-config.yml -u 2610
 Warning: Permanently added 'h-custmgmt-msn-1.binc.net,64.73.42.185' (RSA) to the list of known hosts.
 Enter PASSCODE:
 Executing: ssh -x -F /home/2610/my-ssh-config h-custmgmt-msn-1.binc.net cat /opt/access/dcapps/dcapps-s-bmn09
 Executing: ssh -x -F /home/2610/my-ssh-config h-custmgmt-msn-1.binc.net cat /opt/access/dcapps/dcapps-s-bmn15
 Executing: ssh -x -F /home/2610/my-ssh-config h-custmgmt-msn-1.binc.net cat /opt/access/hcs/hcs-s-bmn03
```

#### 3. Verify that the ssh configuration file is setup:
```
 $ cat ~/my-ssh-config
 ControlMaster auto
 ControlPath ~/.ansible/cp/ansible-ssh-%h-%p-%r
 UserKnownHostsFile /dev/null
 StrictHostKeyChecking no

 Host h-custmgmt-msn-1
   Hostname h-custmgmt-msn-1.binc.net
   User 2610
   ForwardAgent yes
   ControlPersist 5m

 Host hcs-s-bmn03
   User 2610
   Port 42405
   Hostname 172.20.1.1
   ProxyCommand ssh -x -F /home/2610/my-ssh-config -q -W %h:%p h-custmgmt-msn-1
   ForwardAgent yes
   ControlPersist 5m

 Host dcapps-s-bmn09
   User 2610
   Port 44060
   Hostname 172.20.1.1
   ProxyCommand ssh -x -F /home/2610/my-ssh-config -q -W %h:%p h-custmgmt-msn-1
   ForwardAgent yes
   ControlPersist 5m

 Host dcapps-s-bmn15
   User 2610
   Port 51416
   Hostname 172.20.1.1
   ProxyCommand ssh -x -F /home/2610/my-ssh-config -q -W %h:%p h-custmgmt-msn-1
   ForwardAgent yes
   ControlPersist 5m
```

#### 4. Verify that the .ansible.cfg configuration file is setup:
```
 $ cat .ansible.cfg
 [defaults]
 host_key_checking = False

 [ssh_connection]
 ssh_args = -F /home/2610/my-ssh-config
```

#### 5. Open ssh connections to BMNs:
```
 $ connect-to-bmns -c ~/my-ssh-config -b hcs-s-bmn03 -b dcapps-s-bmn09 -b dcapps-s-bmn15
 Executing: ssh -x -F /home/2610/my-ssh-config -N -f hcs-s-bmn03
 Enter PASSCODE:
 Executing: ssh -x -F /home/2610/my-ssh-config -N -f dcapps-s-bmn09
 Warning: Permanently added '[172.20.1.1]:44060' (ECDSA) to the list of known hosts.
 Enter PASSCODE:
 Executing: ssh -x -F /home/2610/my-ssh-config -N -f dcapps-s-bmn15
 Warning: Permanently added '[172.20.1.1]:51416' (ECDSA) to the list of known hosts.
 Enter PASSCODE:
```

#### 6. Setup ansible playbooks and inventory:

Download/Create/Modify Ansible playbooks and the device inventories.
