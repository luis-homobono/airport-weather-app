from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import AirportModel
from schemas.airports import AirportSchema

blp = Blueprint("Airports operations", __name__, description="Endpoints for airports")

@blp.route("/airport")
class AirportView(MethodView):

    @blp.response(HTTPStatus.OK, AirportSchema(many=True))
    def get(self):
        try:
            airports = AirportModel.query.all()
            return airports
        except:
            abort(400, message="Airports empty")
