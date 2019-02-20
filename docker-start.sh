#!/bin/sh

docker build . -t geocodeapi
docker run -it --name srvgeocodeapi --net=rede_paineis --ip=172.18.0.8 geocodeapi
