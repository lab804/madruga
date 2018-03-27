from marshmallow import fields, ValidationError

from project.extensions import marshmallow
from project.api.models import Station


def ensure_unique_identity(data):
    station = Station.find_by_name(data)

    if station:
        raise ValidationError('{0} already exists'.format(data))

    return data


class StationSchema(marshmallow.Schema):
    class Meta:
        fields = ('name', 'latitude', 'longitude')


class CreateStationSchema(marshmallow.Schema):
    name = fields.Str(required=True, validate=ensure_unique_identity)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)


stations_schema = StationSchema(many=True)
add_station_schema = CreateStationSchema()
