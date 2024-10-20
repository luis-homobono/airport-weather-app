from http import HTTPStatus

from flask_smorest import Api
from flask import Flask

from db import db
from cache import cache
from config import DevelopConfig
from resources.tickets import blp as TicketBlueprint
from resources.airports import blp as AirportBlueprint
from resources.healthchecks import blp as HealthcheckBlueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopConfig)
    db.init_app(app=app)
    cache.init_app(app=app)
    api = Api(app=app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(AirportBlueprint)
    api.register_blueprint(TicketBlueprint)
    api.register_blueprint(HealthcheckBlueprint)

    return app
