from marshmallow import fields, Schema


class FlightSchema(Schema):
    airline = fields.Str(required=True)
    flight_num = fields.Int(required=True)
    origin_iata_code = fields.Str(required=True)
    destination_iata_code = fields.Str(required=True)
    create_date = fields.Date(required=True)


class WeatherFlightSchema(Schema):
    airline = fields.Str(required=True)
    flight_num = fields.Int(required=True)
    origin = fields.Dict(keys=fields.Str)
    destination = fields.Dict(keys=fields.Str)
