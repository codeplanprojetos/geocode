#!/bin/sh

docker build . -t geocode-img
docker run -it --name geocode-cnr -p 8001:80 --net=rede_paineis --ip=172.18.0.8 geocode-img
