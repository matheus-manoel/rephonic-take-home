import json
import unittest
from rephonic.factory import create_app
from rephonic.extensions import db


class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app('tests.test_config')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_trigger_scrape(self):
        response = self.client.post('/tasks/get-reviews/podaddict/', json={'id': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['status'], 'background task to scrape 123 started')

    def test_get_reviews(self):
        response = self.client.get('/reviews/podaddict/?podcast_id=123')
        self.assertEqual(response.status_code, 200)
