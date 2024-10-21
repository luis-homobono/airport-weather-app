from http import HTTPStatus

import pandas as pd
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from utils.cache_handler import read_cache
from schemas.tickets import UploadTicketsSchema
from utils.parrallel_process import generate_report
from utils.insert_database import validate_airports, save_data, save_fligths

blp = Blueprint("Tickets operations", __name__, description="Endpoints for tickets")


@blp.route("/ticket/upload-file/")
class UploadTicketsAirportView(MethodView):
    @blp.arguments(UploadTicketsSchema, location="files")
    @blp.response(HTTPStatus.ACCEPTED)
    def post(self, files):
        file = files["file_csv"]
        data = pd.read_csv(file)
        unique_data = data.drop_duplicates(keep=False)
        airports = set(
            list(unique_data["origin_iata_code"].unique())
            + list(unique_data["destination_iata_code"].unique())
        )
        airports_validated = validate_airports(airports)
        cached = read_cache(airports=airports)
        if len(cached) < len(airports_validated):
            responses = save_data(data=data, airports=airports_validated)
            cached.append(responses)

        save_fligths(tickets_data=unique_data)
        return {"message": "Data Uploaded Fine"}
