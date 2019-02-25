#!/bin/bash
# Execute este arquivo para criar um container autocontido com o geocode. 

CWD="$(cd "$(dirname "$0")" && pwd)"
cd $CWD

GEOCODE_IMG=`docker images | egrep 'gu-geocodeapi-img\s*runnable'`

if [[ "x$GEOCODE_IMG" = "x" ]]
then
	echo "Imagem de docker não encontrado, criando..."
	source docker-build-runnable-container.sh
	GEOCODE_IMG=`docker images | egrep 'gu-geocodeapi-img\s*tmp1'`
	echo $GEOCODE_IMG
	if [[ "x$GEOCODE_IMG" = "x" ]]
	then
		echo "Erro ao criar imagem. Verifique a saída do arquivo docker-output.txt"
		exit
	fi
fi

echo "Aguarde: processando endereços..."
docker run -v $CWD:/root gu-geocodeapi-img:runnable /var/www/geocode/geocode.sh --delimitador $1 --campos $2 --arquivo /root/$3
