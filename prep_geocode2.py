# -*- coding: UTF-8 -*-

from json import loads, dumps
import re, string, sys, os
from difflib import SequenceMatcher
from operator import itemgetter
from unicodedata import normalize
from buscas import buscar
from formatacao import formatar_geojson

import encodings.idna


OK, FAIL, INTERRUPTED = 0, -1, -2


class ThreadInterrompidaError(Exception):
    pass


def gera_lista_final(dct_pesquisa, atualiza_progresso=lambda: True):
    '''
    Recebe dicionário com dados do arquivo CSV (lista de dicionários com a chave e com as colunas a serem geocodificadas) e lista de colunas na ordem em que deve ser feita a geocodificação. Monta a lista final que será gravada em novo arquivo csv aplicando a função _consulta_geocode para cada registro.
    '''
    try:
        dados = dct_pesquisa['dados']
        colunas = dct_pesquisa['prioridade']
        geocode_service = dct_pesquisa['geocode_service']
        dados_finais = []
        total = len(dados)
        ct = 1

        for d in dados:
            lb_key = 'KEY'
            key = d[lb_key]
            dct = {lb_key: key}

            for c in colunas:
                if c in list(d.keys()):
                    result_set = _consultar_geocode(d[c], c, geocode_service)
                    dct.update(result_set)
                    if dct['SIMILARIDADE'] != 0.0:
                        break

            dados_finais.append(dct)

            # Atualiza contador de progresso
            if not atualiza_progresso(ct):
                raise ThreadInterrompidaError()
            else:
                print('prep_geocode: {0} de {1}'.format(ct, total))
                ct += 1

        return dados_finais

    except ThreadInterrompidaError as e:
        print('prep_geocode: interrupção por usuário foi detectada: %s' % e)
        raise e

    except Exception as e:
        print('prep_geocode: Erro ao gerar lista final: %s' % e)


def _consultar_geocode(string_pesquisa, coluna, geocode_service):
    '''
    Recebe a string a ser geocodificada e sua coluna correspondente.
    Consulta a API de geocodificação e avalia o resultado, retornando o dicionário que será inserido na lista final.
    '''
    try:
        dct = {}
        encontrou = False

        str_pesquisa = _remove_acentos(string_pesquisa)
        dado_reduzido = _reduz_dado(str_pesquisa)

        for d in dado_reduzido[::-1]:
            geojson = _consultar_local(d, geocode_service)
            resultado_consulta = _avaliar_resultado(d, geojson)

            if resultado_consulta:
                dct.update({'COLUNA_PESQ': coluna, 'DADO_COMPL_PESQ': dado_reduzido[-1], 'DADO_PESQ': d})
                dct.update(resultado_consulta)
                encontrou = True
                break

        if encontrou==False:
            dct.update({'COLUNA_PESQ': 'ALL', 'DADO_COMPL_PESQ': 'ALL', 'DADO_PESQ': 'ALL', 'LONG': 'NOT FOUND', 'LAT': 'NOT FOUND', 'LOCAL_ENCONTRADO': 'NOT FOUND', 'SIMILARIDADE': 0.0})
        return dct

    except Exception as e:
        print('prep_geocode: Erro ao montar novo registro: %s' % e)



def _reduz_dado(dado):
    '''
    Recebe uma string e retorna uma lista com todas as possibilidades de pesquisa (string inteira e suas reduções de até 2 palavras). Ex: 'QD 400 LT B APT 201' => ['QD 400','QD 400 LT','QD 400 LT B','QD 400 LT B APT','QD 400 LT B APT 201']
    '''
    s = dado.replace('.', '').replace(',', ' ').split()
    if len(s) >= 2:
        base = s[0] + ' ' + s[1]
        dados = [base]
        for x in range(2,len(s)):
            base += ' ' + s[x]
            dados.append( base )
        return dados
    else:
        return s


def _consultar_local(local, geocode_service):
    return formatar_geojson(buscar(local, 33))


def testa_conexao(geocode_service):
    '''
    Recebe a descrição de um local e faz a pesquisa do mesmo na API de geocodificação
    '''
    try:
        consulta = geocode_service + '/?{0}' if geocode_service[-1] != '/' else geocode_service + '?{0}'
        parametros = urllib.parse.urlencode({'localidade': '', 'limite': '1'})
        result = urllib.request.urlopen(consulta.format(parametros))
        http_code = result.code
        return OK, http_code, result.read()
    except Exception as e:
        print('prep_geocode: Erro ao consultar API de geocodificação: %s' % e)
        return FAIL, 0, '%s' % e


def _avaliar_resultado(dado_busca, geojson):
    '''
    Recebe a string resultante da consulta à API e a string consultada.
    Retorna dicionário com local encontrado, similaridade e coordenadas (latitude e longitude)
    '''
    try:
        features = geojson['features']

        if features:
            dados = []
            for f in features:
                # nome_local = f['properties']['nome'].encode('utf8')
                nome_local = f['properties']['nome']

                local = {
                    'LOCAL_ENCONTRADO': nome_local,
                    'COORDENADAS': f['geometry']['coordinates']
                }
                dados.append(local)


            for d in dados:
                # similaridade = round(SequenceMatcher(None, d['LOCAL_ENCONTRADO'].ljust(maior).upper(), dado_busca.upper()).ratio(), 5)
                similaridade = round(SequenceMatcher(None, d['LOCAL_ENCONTRADO'].upper(), dado_busca.upper()).ratio(), 5)
                d.update({'SIMILARIDADE': similaridade})

            dados_ordenados = sorted(dados, key=itemgetter('SIMILARIDADE'))
            melhor_resultado = dados_ordenados[-1]
            melhor_resultado.update({'LONG': melhor_resultado['COORDENADAS'][0], 'LAT': melhor_resultado['COORDENADAS'][1]})
            del melhor_resultado['COORDENADAS']

            return melhor_resultado
        else:
            resultado = {}
            return resultado

    except Exception as e:
        print('prep_geocode: Erro ao gerar lista final: %s' % e)


def _remove_acentos(txt):
    '''
    Recebe string e remove toda a acentuação gráfica
    Disponível em: https://wiki.python.org.br/RemovedorDeAcentos
    '''
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def fatia_lista(lista, n):
    '''
    Recebe uma lista e divide-a em n sublistas
    '''
    for i in range(0, len(lista), n):
        yield lista[i:i + n]

