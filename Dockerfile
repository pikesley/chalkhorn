FROM python:3.7

RUN apt-get update && apt-get install -y make

ENV PROJECT chalkhorn

COPY docker-config/bashrc /root/.bashrc
RUN pip install --upgrade pip

WORKDIR /opt/${PROJECT}

COPY ${PROJECT} /opt/${PROJECT}

RUN make install
