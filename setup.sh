#!/bin/bash

sudo apt-get update
sudo apt-get install apache2-dev
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-virtualenv -y
sudo apt-get install unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc

source virtualenv_setup.sh
source pip_setup.sh
