# -*- coding: utf-8 -*-

import csv
import prep_geocode2


def _atualiza_progresso(valor):
    print("\r%d localizações processadas..." % valor)


def run(arquivo, delimitador, campos):
    dados_arquivo_original, colunas_disponiveis = csv.lista_colunas_e_dados(arquivo, delimitador)
    tamanho = len(self._dados_arquivo_original)

    if campos == '*':
        colunas_escolhidas = colunas_disponiveis
    else:
        colunas_escolhidas = campos.split(',')

    colunas = self._colunas_escolhidas[:]
    dados_preparados = csv.prepara_dados(dados_arquivo_original, colunas)
    dados_padronizados = csv.padroniza_dados(dados_preparados)
    csv.gera_arquivo(dados_arquivo_original, 'original', arquivo, colunas_disponiveis)

    # Gera arquivos de saída.
    labels_arquivo_geocode = ['KEY', 'COLUNA_PESQ', 'DADO_COMPL_PESQ', 'DADO_PESQ', 'LOCAL_ENCONTRADO', 'SIMILARIDADE', 'LAT', 'LONG']
    fatias = list(prep_geocode2.fatia_lista(dados_padronizados, tamanho))
    val = 0

    for v in fatias:
        val += 1
        dct_pesquisa = {'prioridade': colunas, 'dados': v, 'geocode_service': None}
        lista_final = prep_geocode2.gera_lista_final(dct_pesquisa, _atualiza_progresso)
        csv.gera_arquivo(lista_final, 'geocode' + str(val), self._arquivo, labels_arquivo_geocode)

    diretorio, arquivo_saida = csv.identifica_diretorio(arquivo)
    print(' * Diretório de saída: ', diretorio)
    print(' * Arquivo gerado: ', arquivo_saida)

