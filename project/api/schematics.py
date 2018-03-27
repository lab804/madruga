from marshmallow import fields
from marshmallow import ValidationError

from project.api.models import Station
from project.extensions import marshmallow


def ensure_unique_identity(data):
    station = Station.find_by_name(data)

    if station:
        raise ValidationError('{0} already exists'.format(data))

    return data


class StationSchema(marshmallow.Schema):
    class Meta(object):
        fields = ('id', 'name', 'latitude', 'longitude')


class CreateStationSchema(marshmallow.Schema):
    name = fields.Str(required=True, validate=ensure_unique_identity)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


station_schema = StationSchema()
add_station_schema = CreateStationSchema()
