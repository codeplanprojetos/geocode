#!/bin/bash

GEOCODE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd $GEOCODE_DIR

abort_on_error()
{
    if [ $? -ne 0 ]; then
        exit $?
    fi
}

# Carrega dados de configuração
CFG_FILE="wsgi.cfg"
VHOST_FILE="geocode.vhost"

VHOST_CONTENTS="$(cat ./config/$VHOST_FILE)"
CFG_CONTENTS="$(cat ./config/$CFG_FILE)"

GEOCODE_ADMIN="$(echo "$VHOST_CONTENTS" | grep "ServerAdmin" | sed "s/^ServerAdmin\s*//")"
if [ "X$GEOCODE_ADMIN" == 'X$GEOCODE_ADMIN' ]; then
    GEOCODE_ADMIN="nobody@localhost"
fi

GEOCODE_SERVER="$(echo "$VHOST_CONTENTS" | grep "ServerName" | sed "s/^ServerName\s*//")"
if [ "X$GEOCODE_SERVER" == 'X$GEOCODE_SERVER' ]; then
    GEOCODE_SERVER="127.0.0.1"
fi

GEOCODE_DBCONN="$(echo "$CFG_CONTENTS" | grep "GEOCODE_DBCONN" | sed "s/^GEOCODE_DBCONN\s*=\s*//")"
if [ "X$GEOCODE_DBCONN" == "X" ]; then
    GEOCODE_DBCONN="postgresql+psycopg2://<LOGIN>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DB_NAME>"
fi

# Coleta de dados para o deploy
GEOCODE_ADMIN="nobody@localhost"
read -p "Defina o e-mail do administrador do serviço [padrão: $GEOCODE_ADMIN]: " USER_GEOCODE_ADMIN
if [ "X$USER_GEOCODE_ADMIN" != "X" ]; then
    GEOCODE_ADMIN=$USER_GEOCODE_ADMIN
fi

GEOCODE_SERVER="127.0.0.1"
read -p "Defina o endereço do servidor HTTP do serviço [padrão: $GEOCODE_SERVER]: " USER_GEOCODE_SERVER
if [ "X$USER_GEOCODE_SERVER" != "X" ]; then
    GEOCODE_SERVER=$USER_GEOCODE_SERVER
fi

cat << EOF > ./config/$VHOST_FILE
WSGIPythonPath $GEOCODE_DIR
<VirtualHost *:80>
        ServerAdmin $GEOCODE_ADMIN
        ServerName $GEOCODE_SERVER

        DocumentRoot $GEOCODE_DIR
        ErrorLog $GEOCODE_DIR/logs/error.log
        CustomLog $GEOCODE_DIR/logs/access.log combined

        WSGIDaemonProcess geocode processes=2 threads=8 display-name=geocode home=$GEOCODE_DIR
        <Directory />
            AuthType None
            Allow from all
        </Directory>

        WSGIScriptAlias / $GEOCODE_DIR/geocode.wsgi
        WSGIProcessGroup geocode
</VirtualHost>
EOF

abort_on_error

VHOST_PATH="/etc/apache2/sites-available/geocode.vhost"
read -p "Defina o caminho absoluto do arquivo de configuração do vhost do Geocode [padrão: $VHOST_PATH]: " USER_VHOST_PATH
if [ "X$USER_VHOST_PATH" != "X" ]; then
    VHOST_PATH=$USER_VHOST_PATH
fi

VHOST_LINK="/etc/apache2/sites-enabled/geocode.vhost"
read -p "Defina o caminho absoluto do LINK para o arquivo de configuração do vhost do Geocode [padrão: $VHOST_LINK]: " USER_VHOST_LINK
if [ "X$USER_VHOST_ENABLED_PATH" != "X" ]; then
    VHOST_ENABLED_PATH=$USER_VHOST_ENABLED_PATH
fi

if [ -e $VHOST_PATH ]; then
    USER_INPUT=""
    while [ "X$USER_INPUT" != 'Xs' ] && [ "X$USER_INPUT" != 'Xn' ]; do
        read -p "Arquivo já existe. Sobrescrever [s/n]?" USER_INPUT
        USER_INPUT="$(echo $USER_INPUT | tr SN sn)"

        if [ "X$USER_INPUT" == 'Xs' ]; then
            cp "./config/$VHOST_FILE" $VHOST_PATH
	    abort_on_error
        fi
    done
else
    cp "./config/$VHOST_FILE" $VHOST_PATH
    abort_on_error
fi

if [ -e $VHOST_LINK ]; then
    if [ ! -L $VHOST_LINK ]; then
        USER_INPUT=""
        while [ "X$USER_INPUT" != 'Xs' ] || [ "X$USER_INPUT" != 'Xn' ]; do
            read -p "Arquivo $VHOST_LINK já existe, mas não é um link. Deseja sobrescrevê-lo como um link [s/n]? " USER_INPUT
            USER_INPUT="$(echo $USER_INPUT | tr SN sn)"

            if [ "X$USER_INPUT" == 'Xs' ]; then
                ln -sf $VHOST_PATH $VHOST_LINK
                abort_on_error
            fi
	done
    else
        ln -sf $VHOST_PATH $VHOST_LINK
        abort_on_error
    fi
else
    ln -sf $VHOST_PATH $VHOST_LINK
    abort_on_error
fi

read -p "Defina a string de conexão com o banco de dados do Geocode [padrão: $GEOCODE_DBCONN]: " USER_GEOCODE_DBCONN
if [ "X$USER_GEOCODE_DBCONN" != "X" ]; then
    GEOCODE_DBCONN=$USER_GEOCODE_DBCONN
fi

# Reescreve arquivo de configuração
cat << EOF > ./config/$CFG_FILE
[env]
GEOCODE_DBCONN = $GEOCODE_DBCONN
EOF

abort_on_error

source virtualenv_setup.sh
source pip_setup.sh
