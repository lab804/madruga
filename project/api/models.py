from flask import current_app
from sqlalchemy import func, asc

from project.extensions import db


class Station(db.Model):
    __tablename__ = "stations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    latitude = db.Column(db.Float(), nullable=False, index=True)
    longitude = db.Column(db.Float(), default=True, index=True)
    is_public = db.Column(db.Boolean(), default=True, nullable=False)
    url = db.Column(db.String(255), nullable=True)

    def __init__(self, name, latitude, longitude, url=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.url = url

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
