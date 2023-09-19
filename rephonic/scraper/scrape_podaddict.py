from ..extensions import celery

@celery.task
def scrape_podcast_reviews(podcast_id):
    # Scrape the podcast reviews here
    print('Scraping podcast reviews')
    pass
