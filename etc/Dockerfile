FROM python:3.6

ADD yamltools/ /home/armory/yamltools
ADD setup.py /home/armory

WORKDIR /home/armory

RUN python3 setup.py install
