import os
from http import HTTPStatus

from flask_smorest import Api
from flask import Flask, jsonify

from db import db
from config import DevelopConfig
from resources.airports import blp as AirportBlueprint
from resources.tickets import blp as TicketBlueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopConfig)
    db.init_app(app=app)
    api = Api(app=app)

    @app.route("/healthcheck")
    def healthcheck():
        return jsonify({"message": "Wheather Airport by Tickets API is running"}), HTTPStatus.OK

    with app.app_context():
        db.create_all()

    api.register_blueprint(AirportBlueprint)
    api.register_blueprint(TicketBlueprint)

    return app
