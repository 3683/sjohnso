FROM alpine:3.3

MAINTAINER Shawn Johnson <sjohnso@gmail.com>

RUN apk add --update \
    bash \
    openssh \
    g++ \
    git \
    libffi-dev \
    openssl-dev \
    python \
    python-dev \
    py-pip \
    sudo \
    sshpass \
    tzdata && \
    pip install --upgrade pip && \
    pip install paramiko PyYAML Jinja2 httplib2 six pywinrm && \
    pip install ansible==2.1.0.0 && \
    rm -rf /var/cache/apk/* /root/.cache && \
    mkdir /etc/ansible && \
    curl -o /etc/ansible/ansible.cfg https://raw.githubusercontent.com/ansible/ansible/devel/examples/ansible.cfg && \
    mkdir /a && \
    cp /usr/share/zoneinfo/CST6CDT /etc/localtime && \
    rm -rf /var/cache/apk/* && \
    rm -f /etc/ssh/ssh_*_key && \
    sed -i "s/^#UsePrivilegeSeparation.*/UsePrivilegeSeparation yes/g" /etc/ssh/sshd_config && \
    sed -i "s/^#UseDNS.*/UseDNS no/g" /etc/ssh/sshd_config && \
    sed -i "s/^#PasswordAuthentication.*/PasswordAuthentication no/g" /etc/ssh/sshd_config && \
    sed -i "s/^#ClientAliveInterval.*/ClientAliveInterval 15/g" /etc/ssh/sshd_config && \
    mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh

VOLUME ["/a"]

ADD run.sh /usr/sbin/run.sh
ADD check-tunnel-status /usr/local/bin/check-tunnel-status
ADD connect-to-bmns /usr/local/bin/connect-to-bmns
ADD create-ssh-config /usr/local/bin/create-ssh-config
ADD keys-from-yaml /usr/local/bin/keys-from-yaml
ADD terminate-ssh /usr/local/bin/terminate-ssh
ADD update-ssh-config-with-hosts /usr/local/bin/update-ssh-config-with-hosts

RUN chmod +x /usr/local/bin/check-tunnel-status /usr/local/bin/connect-to-bmns /usr/local/bin/create-ssh-config /usr/local/bin/keys-from-yaml /usr/local/bin/terminate-ssh /usr/local/bin/update-ssh-config-with-hosts /usr/sbin/run.sh

EXPOSE 22

CMD ["/usr/sbin/run.sh"]
