from marshmallow import fields, Schema


class AirportSchema(Schema):
    iata_code = fields.Str(required=True)
    name = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
