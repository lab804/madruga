import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_station

class TestStationsService(BaseTestCase):
    """Test for the Stations Service."""
    version = '/v1/'

    def test_statios(self):
        """Ensure the /ping route beheves correctly."""
        response = self.client.get(f'{self.version}stations/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_station(self):
        """Ensure a new station can be added to the database."""
        with self.client:
            response = self.client.post(
                f'{self.version}stations',
                data=json.dumps({
                    'name': 'estacao-x',
                    'latitude': -15.789343,
                    'longitude': -47.925756
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('estacao-x was added', data['message'])
            self.assertIn('success', data['status'])

    def test_get_stations(self):
        add_station('estacao-x', -15.789343, -47.925756)
        add_station('estacao-y', -15.789343, -47.925756)
        add_station('estacao-z', -19.789343, -28.925756)

        with self.client:
            response = self.client.get(
                f'{self.version}stations',
                query_string={
                    'lat': -19.789559,
                    'lng': -28.925123
                }
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('data', data)
            self.assertTrue(data['data']['id'])
            self.assertEqual(data['data']['name'], 'estacao-z')
            self.assertEqual(data['data']['latitude'], -19.789343)
            self.assertEqual(data['data']['longitude'], -28.925756)


if __name__ == '__main__':
    unittest.main()
