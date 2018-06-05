# -*- coding: utf-8 -*-

from os import environ, path
from flask import Flask
from flask_restful import Api
from flask_compress import Compress
from flask_cors import CORS
from ambiente import whoosh_base, static_folder, geocode_db
from localizacao import localizacao
from whoosh.analysis import StemmingAnalyzer


def create_app():
    app = Flask(__name__, static_folder=static_folder)
    app.config.from_pyfile('./config/geocode.cfg')
    app.config['SQLALCHEMY_DATABASE_URI'] = geocode_db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    Compress(app)
    print("app criado.")

    from modelos import db
    db.init_app(app)

    from modelos import carregar_base
    carregar_base()
    print("base indexada.")

    api = Api(app)
    localizacao(api)
    print("endpoint de localizacao criado.")

    return app


