FROM python:alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ARG BOT_TOKEN
ENV BOT_TOKEN ${BOT_TOKEN}

ARG SPREADSHEET_ID
ENV SPREADSHEET_ID ${SPREADSHEET_ID}

WORKDIR /SouvenirPerfumeTGBot

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

ADD . /SouvenirPerfumeTGBot

RUN chmod -R 777 ./
