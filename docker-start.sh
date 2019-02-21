#!/bin/bash

CWD="$(cd "$(dirname "$0")" && pwd)"
echo $CWD

docker build . -t gu-geocodeapi-img:tmp1

# Instala pacotes do pip na imagem temporária.
docker run --name tmp-geocodeapi -v $CWD:/var/www/geocode gu-geocodeapi-img:tmp1 /var/www/geocode/docker-pip-install.sh
docker commit tmp-geocodeapi gu-geocodeapi-img:tmp2
docker rm tmp-geocodeapi
docker image rm gu-geocodeapi-img:tmp1

# Reconstrói índice local de endereços na imagem temporária.
docker run --name tmp-geocodeapi -v $CWD:/var/www/geocode gu-geocodeapi-img:tmp2 /var/www/geocode/docker-rebuild-db.sh
docker commit tmp-geocodeapi gu-geocodeapi-img:latest
docker rm tmp-geocodeapi
docker image rm gu-geocodeapi-img:tmp2

# Executa o container como daemon (Ctrl-P + Ctrl-Q faz o detach)
docker run -it --name gu-geocodeapi -v $CMD:/var/www/geocode --net=rede_paineis --ip=172.18.0.8 gu-geocodeapi-img:latest
