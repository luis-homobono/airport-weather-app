from http import HTTPStatus

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from models import FlightModel
from utils.cache_handler import read_cache
from schemas.flights import FlightSchema, WeatherFlightSchema

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


@blp.route("/flights-weather/<string:num_flight>")
class FlightsWeatherView(MethodView):
    @blp.response(HTTPStatus.OK, WeatherFlightSchema(many=True))
    def post(self, num_flight):
        try:
            airports = FlightModel.query.filter_by(flight_num=num_flight)
            airport_response = [airport.__dict__ for airport in airports]
            for airport in airport_response:
                cached = read_cache([airport["destination_iata_code"], airport["origin_iata_code"]])
                airport["destination"] = [airport_cach for airport_cach in cached if airport_cach["code"] == airport["destination_iata_code"]][0]
                airport["origin"] = [airport_cach for airport_cach in cached if airport_cach["code"] == airport["origin_iata_code"]][0]
            return airport_response
        except:
            abort(400, message="Flights weather empty")
