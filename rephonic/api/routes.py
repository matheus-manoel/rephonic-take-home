from flask import Blueprint, request, jsonify, current_app
from rephonic.models.review import Review
from rephonic.scraper.scrape_podaddict import scrape_podcast_reviews

api = Blueprint('api', __name__)


def format_reviews(reviews):
    return [
        {
            "id": review.id,
            "created_date": review.created_date.strftime('%Y-%m-%d'),
            "text_content": review.text_content,
            "author_name": review.author_name
        }
        for review in reviews
    ]

@api.route("/tasks/get-reviews/podaddict/", methods=["POST"])
def trigger_scrape():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    podcast_id = data.get("id")
    if not podcast_id:
        return jsonify({"error": "No podcast ID provided"}), 400
    scrape_podcast_reviews.apply_async(args=[podcast_id])
    return jsonify({"status": f"background task to scrape {podcast_id} started"})

@api.route("/reviews/podaddict/", methods=["GET"])
def get_reviews():
    podcast_id = request.args.get('podcast_id')
    if not podcast_id:
        return jsonify({"error": "No podcast ID provided"}), 400
    
    try:
        with current_app.app_context():
            reviews = (
                Review.query
                .filter_by(podcast_id=podcast_id)
                .order_by(Review.created_date.desc())
                .limit(50)
                .all()
            )
        return jsonify({"reviews": format_reviews(reviews)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

