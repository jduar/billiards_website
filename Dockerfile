FROM python:3.9.1

WORKDIR /app

COPY ./requirements/common.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

ENV PYTHONPATH=$PYTHONPATH:/app/flaskproject

COPY flaskproject /app/flaskproject
