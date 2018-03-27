import json
import unittest

from project.tests.base import BaseTestCase


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


if __name__ == '__main__':
    unittest.main()
