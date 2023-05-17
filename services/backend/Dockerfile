FROM python:3.10-slim AS base

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY migrations .
COPY pyproject.toml .

COPY . /usr/src/app

FROM base as debug

RUN pip install debugpy
RUN pip install tortoise-cli

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
