from marshmallow import fields, Schema
from flask_smorest.fields import Upload


class UploadTicketsSchema(Schema):
    file_csv = Upload()
