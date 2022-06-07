# Dockerfile

# docker image
FROM python:3.9-alpine

# work dir
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy dependencies
COPY requirements.txt .

# psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Solve uvloop issue
RUN apk add build-base \
    && apk add libffi-dev

# Install dependencies
RUN pip install -r requirements.txt

COPY . .
