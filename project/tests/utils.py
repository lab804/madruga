from project.extensions import db
from project.api.models import Station


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
