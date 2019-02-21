#!/bin/sh

docker build . -t gu-geocodeapi-img
docker run -it --name gu-geocodeapi --net=rede_paineis --ip=172.18.0.8 gu-geocodeapi-img
