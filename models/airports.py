from db import db


class AirportModel(db.Model):
    __tablename__ = "airports"

    id = db.Column(db.Integer, primary_key=True)
    iata_code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(
        db.Float(precision=4), unique=False, nullable=False, default=0.0
    )
    longitude = db.Column(
        db.Float(precision=4), unique=False, nullable=False, default=0.0
    )
