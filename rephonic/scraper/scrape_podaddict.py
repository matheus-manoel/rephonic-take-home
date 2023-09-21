import requests
from rephonic.extensions import celery, db
from rephonic.models.review import Review
from flask import current_app
from rephonic.scraper.utils import get_csrf_token, fetch_reviews, parse_reviews


@celery.task
def scrape_podcast_reviews(podcast_id):
    session = requests.Session()
    csrf_token = get_csrf_token(session, podcast_id)
    soup = fetch_reviews(session, csrf_token, podcast_id)
    
    if soup:
        reviews = parse_reviews(soup)
        with current_app.app_context():
            Review.query.filter_by(podcast_id=podcast_id).delete()
            for review_data in reviews:
                review = Review(
                    podcast_id=podcast_id,
                    text_content=review_data['text_content'],
                    created_date=review_data['created_date'],
                    author_name=review_data['author_name']
                )
                db.session.add(review)
            db.session.commit()
