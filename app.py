# -*- coding: utf-8 -*-

from os import environ, path
from flask import Flask
from flask_restful import Api
from flask_compress import Compress
from flask_cors import CORS
from ambiente import whoosh_base, static_folder, geocode_db
from endpoint import root
from whoosh.analysis import StemmingAnalyzer
from whoosh.index import EmptyIndexError


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
    try:
        carregar_base()
        print("base indexada.")
    except EmptyIndexError:
        pass

    api = Api(app)
    root(api)
    print("endpoint criado.")

    return app


