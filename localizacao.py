# -*- coding: utf-8 -*-

from os import path
from flask import jsonify
from flask_restful import reqparse, Resource
from sys import exc_info

from buscas import buscar
from formatacao import formatar_geojson


def localizacao(api):
    print("Adicionando recurso /...")
    api.add_resource(Localizacao, '/')


# Caminho padrão
class Localizacao(Resource):
    '''
    Endpoint de Localizacao.
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('localidade')
    parser.add_argument('limite')

    def get(self):
        print("Localizacao.get chamado...")
        args = Localizacao.parser.parse_args()
        localidade = args['localidade'] or ''
        limite = args['limite']

        return formatar_geojson(buscar(localidade, limite))
