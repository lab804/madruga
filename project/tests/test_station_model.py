import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_station


class TestUserModel(BaseTestCase):

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


if __name__ == '__main__':
    unittest.main()
