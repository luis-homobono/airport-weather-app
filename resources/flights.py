from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import FlightModel
from schemas.flights import FlightSchema, FlightPostSchema

blp = Blueprint("Flights operations", __name__, description="Endpoints for flights")

@blp.route("/flights")
class FlightsView(MethodView):

    @blp.response(HTTPStatus.OK, FlightSchema(many=True))
    def get(self):
        try:
            airports = FlightModel.query.all()
            return airports
        except:
            abort(400, message="Flights empty")
