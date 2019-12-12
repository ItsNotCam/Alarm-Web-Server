FROM ubuntu:19.10

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 python3-pip -y

COPY source/ /acs
RUN pip3 install -r /acs/requirements.txt

VOLUME /acs /acs/config

WORKDIR /acs
ENTRYPOINT ["python3","run.py"]

