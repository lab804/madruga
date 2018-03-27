import os
import json
import unittest

import coverage
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import Station

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py'
    ]
)
COV.start()
app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    stations_obj = []
    if os.path.exists('project/data/estacoes.json'):
        with open('project/data/estacoes.json') as f:
            stations = json.loads(f.read())
            if stations:
                for key in stations.keys():
                    station = stations[key]
                    if 'latitude' and 'longitude' in station:
                        stations_obj.append(
                            Station(name=key,
                                    latitude=float(
                                        station['latitude'].replace(
                                            ',', '.')),
                                    longitude=float(
                                        station['longitude'].replace(
                                            ',', '.')),
                                    url=station['url'])
                        )
    if len(stations_obj) > 0:
        db.session.add_all(stations_obj)
        db.session.commit()


@cli.command()
def test():
    """Runs the test without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('coverage summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
