FROM python:3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk add --update py-pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .