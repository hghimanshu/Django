FROM python:3.7.7-stretch AS base

RUN apt-get update \
    && apt-get --assume-yes --no-install-recommends install \
        build-essential \
        curl \
        jq \
        libgomp1

WORKDIR /app

# upgrade pip version
RUN pip install --no-cache-dir --upgrade pip==21.2.4

ADD ./ ./

RUN pip install -r requirements.txt

FROM base as dev

RUN apt-get update && apt-get install -y wget
