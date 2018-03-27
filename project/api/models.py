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
