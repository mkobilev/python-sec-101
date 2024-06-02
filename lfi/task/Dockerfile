FROM python:3.10.8-slim as python-base
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 PYTHONUNBUFFERED=1
RUN apt-get -y update; apt-get -y install curl

RUN python -m pip install gunicorn

FROM python-base AS runtime

RUN groupadd -g 1001 app && useradd -g 1001 -u 1001 -m -d /app app -s /bin/bash

WORKDIR /app
USER 1001
COPY ./app .
RUN pip3 install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:8888 app:app