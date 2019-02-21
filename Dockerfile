FROM ubuntu:18.04

ENV APPLICATION_ENV production

# Pra funcionar atrás do proxy da CODEPLAN.
# COPY resolv.conf /etc/resolv.conf

RUN apt-get -y update && apt-get -y install python3 python3-pip

COPY . /var/www/geocode
RUN cd /var/www/geocode && pip3 install -r requirements.txt

# Reconstrói banco de dados local de endereços.
RUN export LC_ALL=C.UTF-8
RUN ./geocode --rebuild

ENTRYPOINT cd /var/www/geocode && gunicorn geocode -b 0.0.0.0:80 --pid /tmp/gunicorn.pid --access-logfile /var/www/geocode/logs/access.log --error-logfile /var/www/geocode/logs/error.log
