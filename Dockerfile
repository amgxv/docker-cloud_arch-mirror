FROM alpine:latest
MAINTAINER amgxv

COPY /mirror-utils /mirror
WORKDIR /mirror

RUN apk update
RUN apk add python3 rsync
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "fetch_mirror.py"]




