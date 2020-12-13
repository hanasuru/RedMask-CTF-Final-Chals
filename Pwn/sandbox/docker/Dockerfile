FROM ubuntu:20.04

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y xinetd && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf
COPY sandbox /home/ctf/
COPY user /home/ctf/
COPY run.sh /home/ctf/
COPY ini_flagnya_gan.txt /home/ctf/
COPY chall /etc/xinetd.d/

EXPOSE 1337

CMD xinetd -dontfork