from flask import Blueprint, request, jsonify
from ..scraper.scrape_podaddict import scrape_podcast_reviews


api = Blueprint('api', __name__)


@api.route("/tasks/get-reviews/podaddict/", methods=["POST"])
def trigger_scrape():
    data = request.json
    podcast_id = data.get("id") if data else None
    task = scrape_podcast_reviews.apply_async(args=[podcast_id])
    return jsonify({"status": "task started", "task_id": str(task.id)})

@api.route("/reviews/podaddict/", methods=["GET"])
def get_reviews():
    podcast_id = request.args.get('podcast_id')
    return jsonify({"status": "fetching reviews", "podcast_id": podcast_id})
