import datetime

from db import db


class FlightModel(db.Model):
    __tablename__ = "flights"

    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(10), nullable=False)
    flight_num = db.Column(db.Integer)
    origin_iata_code = db.Column(db.String(10), nullable=False)
    destination_iata_code = db.Column(db.String(10), nullable=False)
    create_date = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.now(datetime.UTC)
    )
