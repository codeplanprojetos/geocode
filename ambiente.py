# -*- coding: utf-8 -*-

from os import environ, sep, path, getcwd

class UndefinedEnvVarError(Exception):
    '''
    Variável de ambiente necessária para o funcionamento do sistema não definida.
    '''
    def __init__(self, envVar):
        self.message = 'undefined environment variable %s' % envVar


class RelativePathTypeError(Exception):
    '''
    Tipo de caminho precisa ser absoluto.
    '''
    def __init__(self, path):
        self.message = 'absolute path required in "%s"' % path


#
# Verifica variáveis de ambiente obrigatórias.
#

if 'GEOCODE_DBCONN' in environ.keys():
    geocode_db = environ['GEOCODE_DBCONN']
else:
    raise UndefinedEnvVarError('GEOCODE_DBCONN')

if 'GEOCODE_WHOOSHDIR' in environ.keys():
    if environ['GEOCODE_WHOOSHDIR'].startswith(sep):
        whoosh_base = environ['WHOOSH_BASE']
    else:
        whoosh_base = path.join(getcwd(), environ['GEOCODE_WHOOSHDIR'])
else:
    whoosh_base = path.join(getcwd(), 'whoosh_index')

static_folder = path.join(getcwd(), environ.get('GEOCODE_STATICDIR', 'static'))

#if 'GEOCODE_ANALYZER' in environ.keys():
#    whoosh_analyzer = environ['GEOCODE_ANALYZER']
