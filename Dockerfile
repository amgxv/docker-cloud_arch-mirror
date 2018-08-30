FROM alpine:latest
MAINTAINER amgxv

COPY /mirror-utils /mirror
RUN mv /mirror/root /etc/crontabs/root
WORKDIR /mirror
RUN chmod +x fetch_mirror.py
RUN chmod +x bestmirror.py

RUN apk update
RUN apk add python3 rsync
RUN pip3 install -r requirements.txt

ENTRYPOINT ["crond", "-f"]




