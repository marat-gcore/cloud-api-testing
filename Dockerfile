FROM python:3.12-slim

RUN apt-get update && apt-get install -y openjdk-17-jdk-headless \
    wget \
    unzip \
    && wget https://github.com/allure-framework/allure2/releases/download/2.28.0/allure-2.28.0.zip \
    && unzip allure-2.28.0.zip -d /opt/ \
    && ln -s /opt/allure-2.28.0/bin/allure /usr/bin/allure \
    && rm allure-2.28.0.zip

WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt
