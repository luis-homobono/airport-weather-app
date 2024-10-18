import os
from http import HTTPStatus

from flask import Flask, jsonify

from config import DevelopConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopConfig)

    @app.route("/healthcheck")
    def home():
        return jsonify({"message": "Wheather Airport by Tickets API is running"}), HTTPStatus.OK


    return app