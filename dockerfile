FROM alpine:3.7
COPY ./src /application/
COPY ./requirements.txt /application
COPY ./out /application
WORKDIR /application
RUN apk add make automake gcc g++ python3-dev py3-pip nano\
        && rm -rf /var/lib/apk/lists/*
RUN pip3 install -r requirements.txt