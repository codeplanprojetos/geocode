#!/bin/sh

docker build . -t geocode-img
docker run -it --name geocode-cnr -p 8001:80 geocode-img
