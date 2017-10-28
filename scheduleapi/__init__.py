#! ../env/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Kjetil Andre Liknes'
__email__ = 'kliknes@gmail.com'
__version__ = '0.1'

from flask import Flask
from flask_cors import CORS
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask_security import Security, MongoEngineUserDatastore
from flask_restful import Api

from scheduleapi.controllers.main import main
from scheduleapi import assets
from scheduleapi.models import db, User, Role

from scheduleapi.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager
)


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. scheduleapi.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)

    CORS(app)

    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    app.user_datastore = user_datastore

    # initialize the cache
    cache.init_app(app)

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # initialize SQLAlchemy
    db.init_app(app)

    login_manager.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    # register our blueprints
    app.register_blueprint(main)

    api = Api(app)

    return app
