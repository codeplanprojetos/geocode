#!/bin/sh

docker build . -t geocode-img
docker run -it --name geocode-cnr -p 8000:80 geocode-img
