FROM ubuntu:18.04

ENV APPLICATION_ENV production

# Pra funcionar atrás do proxy da CODEPLAN.
# COPY resolv.conf /etc/resolv.conf

RUN apt-get -y update && apt-get -y install wget git python3 python3-pip python-setuptools nginx virtualenv

COPY config/default.nginx /etc/nginx/sites-enabled/default
COPY . /var/www/geocode

RUN cd /var/www/geocode && pip3 install -r requirements.txt

EXPOSE 8000

ENTRYPOINT service nginx start && cd /var/www/geocode && gunicorn geocode -b 127.0.0.1:8000 --pid /tmp/gunicorn.pid --workers=8
