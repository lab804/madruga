from project.api.models import Station
from project.extensions import db


def add_station(name, latitude, longitude, url=None):
    station = Station(
        name=name,
        latitude=latitude,
        longitude=longitude,
        url=url
    )
    db.session.add(station)
    db.session.commit()
    return station
