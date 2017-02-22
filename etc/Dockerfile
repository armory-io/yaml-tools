FROM python:3.6

ADD armory/ /home/armory/armory
ADD setup.py /home/armory

WORKDIR /home/armory

RUN python3 setup.py install
