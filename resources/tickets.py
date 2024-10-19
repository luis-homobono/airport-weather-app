from http import HTTPStatus

import pandas as pd
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import db
from models import AirportModel
from schemas.tickets import UploadTicketsSchema
from utils.insert_database import validate_airports, save_data

blp = Blueprint("Tickets operations", __name__, description="Endpoints for tickets")

@blp.route("/ticket/upload-file/")
class UploadTicketsAirportView(MethodView):
    @blp.arguments(UploadTicketsSchema, location='files')
    @blp.response(HTTPStatus.ACCEPTED)
    def post(self, files):
        file = files["file_csv"]
        data = pd.read_csv(file)
        airports = set(list(data["origin_iata_code"].unique()) + list(data['destination_iata_code'].unique()))
        airports_validated = validate_airports(airports)
        if len(airports_validated) > 0:
            print("SAVE DATA")
            save_data(data=data, airports=airports_validated)

        return {"message": "Data Uploaded Fine"}
