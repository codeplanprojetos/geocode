# -*- coding: utf-8 -*-

from os import path, mkdir
from whoosh import index
from whoosh.fields import Schema, TEXT, NUMERIC, STORED
from whoosh.support.charset import accent_map
from whoosh.analysis import StemmingAnalyzer, StandardAnalyzer, CharsetFilter
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
from shapely import wkb
from json import loads
from shutil import rmtree

from ambiente import geocode_db, whoosh_base


db = SQLAlchemy()
analyzer = StemmingAnalyzer() | CharsetFilter(accent_map)
schema = Schema(id = NUMERIC, nome=TEXT(analyzer = analyzer, stored = True), geom = STORED)


class Poligono(db.Model):
    __tablename__ = 'openLS_localizacaopoligono'
    __searchable__ = ['nome']
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Unicode)
    geom = db.Column(Geometry('POLYGON'))


class Linha(db.Model):
    __tablename__ = 'openLS_localizacaolinha'
    __searchable__ = ['nome']
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Unicode)
    geom = db.Column(Geometry('LINESTRING'))


class Ponto(db.Model):
    __tablename__ = 'openLS_localizacaoponto'
    __searchable__ = ['nome']
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Unicode)
    geom = db.Column(Geometry('POINT'))

modelos_padroes = [Ponto, Poligono, Linha]


def apagar_base():
    print("Apagando a base...")
    rmtree(whoosh_base)


def criar_base():
    indices = []

    for modelo in modelos_padroes:
        indice = index.create_in(whoosh_base, schema = schema, indexname = modelo.__tablename__)
        indices.append(indice)

    return indices


def wkb2ponto(geometry):
    point = wkb.loads(bytes(geometry.data))
    return point.centroid.x, point.centroid.y


def popular_base():
    sessao = criar_sessao()
    total = 0

    for modelo in modelos_padroes:
        indice = index.open_dir(whoosh_base, schema = schema, indexname = modelo.__tablename__)
        itens = sessao.query(modelo)
        writer = indice.writer()

        for item in itens:
            writer.add_document(id = item.id, nome = item.nome, geom = wkb2ponto(item.geom))
            total += 1

        writer.commit()

    print("Fim da inserção de índices com %d registros." % total)


def carregar_base():
    print("Carregando base...")
    indices = []

    if not path.exists(whoosh_base):
        mkdir(whoosh_base)
        indices = criar_base()
        popular_base()
    else:
        for modelo in modelos_padroes:
            indices.append(index.open_dir(whoosh_base, schema = schema, indexname = modelo.__tablename__))

    print("Carregando base... OK")
    return indices


def criar_sessao():
    engine = create_engine(geocode_db)
    Session = sessionmaker(bind=engine)
    return Session()

