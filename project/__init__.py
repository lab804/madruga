import os

from flask import Flask
from flask_cors import CORS

from project.extensions import (
    db,
    migrate
)
from project.api.v1.stations import StationsView


def extensions_app(app):
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return True


def register_blueprint(app):
    StationsView.register(app)
    return True


def create_app(script_info=None):
    app = Flask(__name__)
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    extensions_app(app)
    register_blueprint(app)

    app.shell_context_processor({'app': app, 'db': db})
    return app
