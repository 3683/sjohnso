#### Build

Create the docker image.

```sh
docker build -t azure-cli:0.9.10 .
```

#### Copy scripts

Copy the wrapper scripts into `/usr/local/bin`.

```sh
cp -p azure /usr/local/bin
cp -p docker-azure-cli /usr/local/bin
chmod 0755 /usr/local/bin/{azure,docker-azure-cli}
```

#### Setup sudo

Add the following lines to `/etc/sudoers` by using `visudo`.

```sh
## Allows members of the docker group to run docker wrapper scripts
%docker	ALL=(ALL) NOPASSWD: /usr/local/bin/docker-azure-cli
```

#### Usage

```sh
$ whoami
nonrootuser
$ which azure
/usr/local/bin/azure
$ azure config mode arm
info:    New mode is arm
```
