FROM python:3.9-bullseye

RUN curl -s http://nginx.org/keys/nginx_signing.key | apt-key add -
RUN echo "deb http://nginx.org/packages/debian/ bullseye nginx" >> /etc/apt/sources.list
RUN echo "deb-src http://nginx.org/packages/debian/ bullseye nginx" >> /etc/apt/sources.list

RUN apt-get update -yqq && apt-get install -yqq nginx
RUN apt-get install libpq-dev python3-dev -y

WORKDIR /app
COPY ./app /app

RUN pip3 install -U pip; pip3 install -r /app/requirements.txt 

RUN rm /etc/nginx/nginx.conf
COPY ./app/nginx.conf /etc/nginx/

EXPOSE 80

RUN chmod +x entrypoint.sh
CMD ["./entrypoint.sh"]
