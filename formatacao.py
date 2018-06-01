# -*- coding: utf-8 -*-


def formatar_geojson(itens):
    '''
    itens é uma lista de tuplas na forma [(nome, coordenadas)]
    '''
    features = []

    for item in itens:
        features.append({'geometry': {'type': 'Point', 'coordinates': item[1]}, 'properties': {'nome': item[0]}, 'type': 'Feature'})

    return {'type': 'FeatureCollection', 'features': features}

