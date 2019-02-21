# -*- coding: utf-8 -*-

import arquivo
import prep_geocode2


def _atualiza_progresso(valor):
    print("\r%d localizações processadas..." % valor); return True


def run(nome_arquivo, delimitador, campos):
    dados_arquivo_original, colunas_disponiveis = arquivo.lista_colunas_e_dados(nome_arquivo, delimitador, 'latin1')
    tamanho = len(dados_arquivo_original)

    if campos == '*':
        colunas_escolhidas = colunas_disponiveis
    else:
        colunas_escolhidas = campos.split(',')

    colunas = colunas_escolhidas[:]
    dados_preparados = arquivo.prepara_dados(dados_arquivo_original, colunas)
    dados_padronizados = arquivo.padroniza_dados(dados_preparados)
    arquivo.gera_arquivo(dados_arquivo_original, 'original', nome_arquivo, colunas_disponiveis)

    # Gera arquivos de saída.
    labels_arquivo_geocode = ['KEY', 'COLUNA_PESQ', 'DADO_COMPL_PESQ', 'DADO_PESQ', 'LOCAL_ENCONTRADO', 'SIMILARIDADE', 'LAT', 'LONG']
    fatias = list(prep_geocode2.fatia_lista(dados_padronizados, tamanho))
    val = 0

    for v in fatias:
        val += 1
        dct_pesquisa = {'prioridade': colunas, 'dados': v, 'geocode_service': None}
        lista_final = prep_geocode2.gera_lista_final(dct_pesquisa, _atualiza_progresso)
        arquivo.gera_arquivo(lista_final, 'geocode' + str(val), nome_arquivo, labels_arquivo_geocode)

    diretorio, arquivo_saida = arquivo.identifica_diretorio(nome_arquivo)
    print(' * Diretório de saída: ', diretorio)
    print(' * Arquivo gerado: ', arquivo_saida)

