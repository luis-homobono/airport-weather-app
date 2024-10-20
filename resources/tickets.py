from http import HTTPStatus

import pandas as pd
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas.tickets import UploadTicketsSchema
from utils.insert_database import validate_airports, save_data, save_fligths

blp = Blueprint("Tickets operations", __name__, description="Endpoints for tickets")

@blp.route("/ticket/upload-file/")
class UploadTicketsAirportView(MethodView):
    @blp.arguments(UploadTicketsSchema, location='files')
    @blp.response(HTTPStatus.ACCEPTED)
    def post(self, files):
        file = files["file_csv"]
        data = pd.read_csv(file)
        unique_data = data.drop_duplicates(keep=False)
        airports = set(list(unique_data["origin_iata_code"].unique()) + list(unique_data['destination_iata_code'].unique()))
        airports_validated = validate_airports(airports)
        if len(airports_validated) > 0:
            print("SAVE DATA")
            save_data(data=data, airports=airports_validated)

        save_fligths(tickets_data=unique_data)

        return {"message": "Data Uploaded Fine"}
