FROM ubuntu:18.04

ENV APPLICATION_ENV production

# Pra funcionar atrás do proxy da CODEPLAN.
# COPY resolv.conf /etc/resolv.conf

RUN apt-get -y update && apt-get -y install python3 python3-pip

COPY requirements.txt /var/www/
RUN pip3 install -r /var/www/requirements.txt

ENTRYPOINT cd /var/www/geocode && LC_ALL=C.UTF-8 gunicorn geocode -b 0.0.0.0:80 --pid /tmp/gunicorn.pid --access-logfile /var/www/geocode/logs/access.log --error-logfile /var/www/geocode/logs/error.log
