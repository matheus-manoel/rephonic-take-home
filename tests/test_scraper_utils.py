import unittest
from unittest.mock import patch, Mock
from datetime import datetime
from bs4 import BeautifulSoup
from rephonic.scraper.utils import get_csrf_token, fetch_reviews, parse_reviews

class TestScraperUtils(unittest.TestCase):

    @patch('requests.Session.get')
    @patch('rephonic.scraper.utils.BeautifulSoup')
    def test_get_csrf_token(self, mock_soup, mock_get):
        # Test case when CSRF token is found
        mock_response = Mock()
        mock_get.return_value = mock_response
        mock_response.text = 'some_html'
        mock_script = Mock()
        mock_script.string = "var csrf_token = 'abc123'"
        mock_soup.return_value.find.return_value = mock_script
        csrf_token = get_csrf_token(Mock(), 'some_podcast_id')
        self.assertEqual(csrf_token, 'abc123')

        # Test case when CSRF token is not found
        mock_soup.return_value.find.return_value = None
        csrf_token = get_csrf_token(Mock(), 'some_podcast_id')
        self.assertEqual(csrf_token, '')

    @patch('requests.Session.post')
    def test_fetch_reviews(self, mock_post):
        # Test case when status_code is 200
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = 'some_html'
        mock_post.return_value = mock_response
        mock_session = Mock()
        mock_session.post.return_value = mock_response
        soup = fetch_reviews(mock_session, 'csrf_token', 'podcast_id')
        self.assertIsNotNone(soup)  # Should pass now

        # Test case when status_code is not 200
        mock_response.status_code = 404
        soup = fetch_reviews(mock_session, 'csrf_token', 'podcast_id')
        self.assertIsNone(soup)

    def test_parse_reviews(self):
        # Test case with review
        sample_html = '''
        <div class="cellcontent">
            <div class="caption2"><span>Username</span><span>Apr 16 2020</span></div>
            <div class="lighttext">Great podcast!</div>
        </div>
        '''
        soup = BeautifulSoup(sample_html, 'html.parser')
        reviews = parse_reviews(soup)
        expected_review = {
            'author_name': 'Username',
            'created_date': datetime(2020, 4, 16),
            'text_content': 'Great podcast!'
        }
        self.assertEqual(reviews[0], expected_review)

        # Test case without review
        sample_html = '<div></div>'
        soup = BeautifulSoup(sample_html, 'html.parser')
        reviews = parse_reviews(soup)
        self.assertEqual(reviews, [])
