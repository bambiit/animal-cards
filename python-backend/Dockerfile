FROM ubuntu:18.04

LABEL maintainer="Bui Minh <minh.bui@helsinki.fi>"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip libpcre3 libpcre3-dev
RUN pip3 install uwsgi

RUN mkdir -p /www/api/animalcards/
WORKDIR /www/api/animalcards/
COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "uwsgi", "--ini --log-master", "app.ini" ]