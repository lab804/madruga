import unittest

from sqlalchemy.exc import IntegrityError

from project.extensions import db
from project.api.models import Station
from project.tests.base import BaseTestCase
from project.tests.utils import add_station


class TestStationModel(BaseTestCase):

    def test_add_station(self):
        station = add_station('estacao-x', -15.789343, -47.925756)
        self.assertTrue(station.id)
        self.assertEqual(station.name, 'estacao-x')
        self.assertEqual(station.latitude, -15.789343)
        self.assertEqual(station.longitude, -47.925756)
        self.assertIsNone(station.url)
        self.assertTrue(station.is_public)

    def test_add_station_url(self):
        station = add_station(
            'estacao-x', -15.789343, -47.925756, 'http://labmet.com.br')
        self.assertTrue(station.id)
        self.assertEqual(station.name, 'estacao-x')
        self.assertEqual(station.latitude, -15.789343)
        self.assertEqual(station.longitude, -47.925756)
        self.assertEqual(station.url, 'http://labmet.com.br')
        self.assertTrue(station.is_public)

    def test_add_station_duplicate_name(self):
        add_station('estacao-x', -15.789343, -47.925756)
        duplicate_station = Station(
            name='estacao-x',
            latitude=-15.789341,
            longitude=-47.925752,
        )
        db.session.add(duplicate_station)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_find_station_by_name(self):
        add_station('estacao-x', -15.789343, -47.925756)
        station = Station.find_by_name('estacao-x')
        self.assertTrue(station.id)
        self.assertEqual(station.name, 'estacao-x')
        self.assertEqual(station.latitude, -15.789343)
        self.assertEqual(station.longitude, -47.925756)
        self.assertIsNone(station.url)
        self.assertTrue(station.is_public)

    def test_find_station_by_location(self):
        add_station('estacao-x', -15.789343, -47.925756)
        add_station('estacao-y', -15.789343, -47.925756)
        add_station('estacao-z', -19.789343, -28.925756)

        station = Station.location(latitude=-19.789559, longitude=-28.925123)
        self.assertTrue(station.id)
        self.assertEqual(station.name, 'estacao-z')
        self.assertEqual(station.latitude, -19.789343)
        self.assertEqual(station.longitude, -28.925756)
        self.assertTrue(station.is_public)


if __name__ == '__main__':
    unittest.main()
