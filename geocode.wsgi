from configparser import ConfigParser
from os import path
from os import environ

if path.exists('./config/wsgi.cfg'):
    config = ConfigParser()
    config.read('./config/wsgi.cfg')

    for key in config['env']:
        environ[key.upper()] = config['env'][key]

activate_this = path.join(environ['GEOCODE_DIR'], 'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
sys.path.insert(0, environ['GEOCODE_DIR'])


# Apaga base se executar da linha de comando.
if __name__ == '__main__':
    from modelos import apagar_base, criar_base
    apagar_base()
    criar_base()
else:
    from app import create_app
    application = create_app()
