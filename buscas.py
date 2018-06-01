# -*- coding: utf-8 -*-

from whoosh.qparser import QueryParser, FuzzyTermPlugin
from shapely import wkb
from json import loads

from modelos import schema, carregar_base, modelos_padroes, criar_sessao


def criar_parser():
    parser = QueryParser('nome', schema)
    parser.add_plugin(FuzzyTermPlugin())
    return parser


def buscar(nome, limite = None, modelos = modelos_padroes):
    indices = carregar_base()
    session = criar_sessao()
    parser = criar_parser()
    expressao = parser.parse(nome)
    resultados = []
    
    if not nome is None:
        for indice in indices:
            with indice.searcher() as searcher:

                if limite == '0':
                    limite = None
                elif type(limite) == str:
                    limite = int(limite)

                resultado = list(searcher.search(expressao, limit=limite))
                resultados += [(item['nome'], item['geom']) for item in resultado]

    return resultados

