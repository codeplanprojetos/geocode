#!/bin/bash

CWD="$(cd "$(dirname "$0")" && pwd)"

#cp /etc/resolv.conf ./resolv.conf

# Apagando imagens e containers antigos.
docker stop gu-geocodeapi 2>/dev/null
docker rm gu-geocodeapi 2>/dev/null
docker image rm gu-geocodeapi-img 2>/dev/null
echo "Construindo imagem gu-geocodeapi.img..."
docker build . -t gu-geocodeapi-img:latest

# Executa servidor gunicorn.
echo "Executando servidor gunicorn."
docker run --detach=true --name gu-geocodeapi -v $CWD:/var/www/geocode --net=rede_paineis --ip=172.18.0.8 gu-geocodeapi-img:latest

# Instala pacotes do pip na imagem temporária.
echo "Aguarde: construindo índice local de endereços..."
docker exec -v $CWD:/var/www/geocode gu-geocodeapi-img:tmp1 gu-geocodeapi /var/www/geocode/docker-rebuild-db.sh
