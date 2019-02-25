#!/bin/bash
# Execute este arquivo para criar um container autocontido com o geocode. 

CWD="$(cd "$(dirname "$0")" && pwd)"
cd $CWD

GEOCODE_IMG=`docker images | egrep 'gu-geocodeapi-img\s*runnable'`

if [[ "x$GEOCODE_IMG" = "x" ]]
then
	echo "Imagem de docker não encontrado, criando..."
	docker build -f Dockerfile-runnable-container -t gu-geocodeapi-img:tmp1 .
	# &> ./docker-output.txt
	GEOCODE_IMG=`docker images | egrep 'gu-geocodeapi-img\s*tmp1'`
	echo $GEOCODE_IMG
	if [[ "x$GEOCODE_IMG" = "x" ]]
	then
		echo "Erro ao criar imagem. Verifique a saída do arquivo docker-output.txt"
		exit
	fi
fi

echo "Aguarde: construindo índice local de endereços..."
docker run --name=gu-geocodeapi-tmp gu-geocodeapi-img:tmp1 /var/www/geocode/docker-rebuild-db.sh
docker commit gu-geocodeapi-tmp gu-geocodeapi-img:runnable
docker rm gu-geocodeapi-tmp
