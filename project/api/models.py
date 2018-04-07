from collections import OrderedDict

from flask import current_app
from sqlalchemy import func, asc

from labmet_libraries.crawlers import INMET
from project.extensions import db


class Station(db.Model):
    TYPE = OrderedDict([
        ('labmet', 'LabMet'),
        ('inmet', 'INMET')
    ])

    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum(*TYPE, name='station_types', native_enum=False),
                     index=True, nullable=False, server_default='labmet')
    model = db.Column(db.String(10), nullable=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    latitude = db.Column(db.Float(), nullable=False, index=True)
    longitude = db.Column(db.Float(), default=True, index=True)
    is_public = db.Column(db.Boolean(), default=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)

    def __init__(self, **kwargs):
        super(Station, self).__init__(**kwargs)

    @classmethod
    def find_by_name(cls, identity):
        return Station.query.filter(Station.name == identity).first()

    @classmethod
    def location(cls, latitude, longitude,
                 distance=None):
        if not distance:
            distance = current_app.config.get('MINIMUM_DISTANCE')
        stations = Station.query.filter(
            func.acos(func.sin(func.radians(
                latitude)) * func.sin(
                func.radians(Station.latitude)) + func.cos(
                func.radians(latitude)) * func.cos(
                func.radians(Station.latitude)) * func.cos(
                func.radians(Station.longitude) - (func.radians(
                    longitude)))) * 6371 <= distance)
        stations.order_by(
            asc(func.acos(func.sin(func.radians(
                latitude)) * func.sin(
                func.radians(Station.latitude)) + func.cos(
                func.radians(latitude)) * func.cos(
                func.radians(Station.latitude)) * func.cos(
                func.radians(Station.longitude) - (func.radians(
                    longitude)))) * 6371))
        return stations.first()

    def weather(self, start, end):
        if self.is_public:
            inmet = INMET()
            data = inmet.get_data(self.url, start, end)
            if data:
                return data
            else:
                return None
        # get internal stations
        else:
            return None
