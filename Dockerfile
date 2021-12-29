FROM python:3.9.5-slim

RUN mkdir -p /usr/src/service
WORKDIR /usr/src/service


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir ./staticfiles

EXPOSE 8000

COPY ./media ./media
COPY ./djangoInstagram ./djangoInstagram
COPY ./instagram ./instagram
COPY ./templates ./templates
COPY ./manage.py .