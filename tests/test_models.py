import unittest
from datetime import datetime
from rephonic.factory import create_app, db
from rephonic.models.review import Review

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app('tests.test_config')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_review(self):
        review = Review(podcast_id='123', author_name="John", text_content="Great podcast!", created_date=datetime.now())
        db.session.add(review)
        db.session.commit()
        self.assertIsNotNone(review.id)

