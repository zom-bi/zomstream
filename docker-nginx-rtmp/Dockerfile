FROM debian:bullseye
MAINTAINER Chris <bsod@zom.bi>
VOLUME ["/usr/local/nginx/conf"]
EXPOSE 8080
ADD nginx_signing.key /tmp/nginx.key
RUN \
      apt-get update &&\
      apt-get install -y gnupg && \
      apt-key add /tmp/nginx.key && \
      echo "deb http://nginx.org/packages/debian/ buster nginx" >> /etc/apt/sources.list && \
      echo "deb-src http://nginx.org/packages/debian/ buster nginx" >> /etc/apt/sources.list && \
      apt-get update &&\
      apt-get build-dep -y nginx && \
      apt-get install -y git
RUN \
      mkdir -pv /opt/nginx/ && \
      cd /opt/nginx/ && \
      apt-get source nginx && \
      git clone https://github.com/winshining/nginx-http-flv-module.git --depth=1
RUN \
      cd /opt/nginx/nginx-* && \
      ./configure --add-module=/opt/nginx/nginx-http-flv-module --with-http_ssl_module && \
      make && \
      make install

ENTRYPOINT ["/usr/local/nginx/sbin/nginx"]
