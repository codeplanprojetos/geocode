# Geocode

Servidor WSGI Python com Flask e Whoosh para acessar serviço de geolocalização da CODEPLAN

## Pré-requisitos

* GNU/Linux
* Apache 2
* Python 3.x
* Flask
* Pypi
* Virtualenv

### Debian e derivados

Se você estiver usando Debian/Ubuntu ou derivados, você pode instalar as dependências acima com os comandos:

```
sudo apt-get update
sudo apt-get install apache2 apache2-dev python3 python3-pip libapache2-mod-wsgi-py3 python-virtualenv
```

Se você estiver usando uma versão muito velha do apache2, talvez seja necessário atualizar o mod_wsgi para apontar para o Python 3 ao invés do Python 2:
```
sudo a2dismod wsgi
sudo apt-get remove libapache2-mod-wsgi
sudo apt-get install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
```

## Instalação

Instale os softwares especificados acima de acordo com a sua distro e execute o comando ``setup.sh`` na pasta raiz e respondendo todas as perguntas que aparecerem. Depois é necessário criar o cache local do Whoosh executando o script ``rebuild.sh``.

