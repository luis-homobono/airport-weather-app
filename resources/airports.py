from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import AirportModel
from utils.cache_handler import read_cache
from schemas.airports import AirportSchema, WeatherAirportSchema

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


@blp.route("/airport-weather/<string:airport_iata_code>")
class AirportWeatherView(MethodView):
    @blp.response(HTTPStatus.OK, WeatherAirportSchema)
    def post(self, airport_iata_code):
        try:
            airports = AirportModel.query.filter_by(iata_code=airport_iata_code)
            airport_response = [airport.__dict__ for airport in airports][0]
            cached = read_cache([airport_response["iata_code"]])
            airport_response["weather"] = cached[0]
            return airport_response
        except:
            abort(400, message="Flights empty")
