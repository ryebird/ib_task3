FROM alpine:latest

RUN apk update && apk add --no-cache \
    build-base gcc musl-dev cmake git json-c-dev libwebsockets-dev \
    libuv-dev zlib-dev openssl-dev vim nano curl wget tree htop \
    bash coreutils findutils procps util-linux

RUN git clone https://github.com/tsl0922/ttyd.git /tmp/ttyd \
    && cd /tmp/ttyd && mkdir build && cd build \
    && cmake .. && make && make install && rm -rf /tmp/ttyd

WORKDIR /app
COPY src/ /app/src/
COPY scripts/ /app/scripts/

RUN gcc -o /app/linux_tasks /app/src/linux_tasks.c \
    && chmod +x /app/scripts/start.sh /app/linux_tasks \
    && adduser -D -s /bin/bash linuxuser

EXPOSE 7681
CMD ["/app/scripts/start.sh"]
