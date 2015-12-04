FROM alpine:3.2

MAINTAINER Shawn Johnson <sjohnso@gmail.com>

ENV AZURE_VERSION 0.9.10

RUN apk update && \
    apk add --update bash g++ make nodejs python && \
    rm -rf /var/cache/apk/* && \
    npm install --global azure-cli@0.9.10 && \
    addgroup dev && \
    adduser -G dev dev -D -h /home/dev && \
    mkdir -p /home/dev && \
    chown -R dev:dev /home/dev

VOLUME ["/home/dev"]

ENV HOME /home/dev
USER dev
WORKDIR /home/dev

ENTRYPOINT ["/usr/bin/azure"]
CMD ["--help"]
