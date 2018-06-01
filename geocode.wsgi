from configparser import ConfigParser
from os import path
from os import environ

if path.exists('./config/wsgi.cfg'):
    config = ConfigParser()
    config.read('/var/www/geocode/wsgi.cfg')

    for key in config['env']:
        environ[key.upper()] = config['env'][key]

activate_this = path.join(environ['GEOCODE_DIR'], 'flask/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, environ['GEOCODE_DIR'])

from geocode import create_app
application = create_app()

# Apaga base se executar da linha de comando.
if __name__ == '__main__':
    from modelos import apagar_base, carregar_base
    apagar_base()
    carregar_base()
