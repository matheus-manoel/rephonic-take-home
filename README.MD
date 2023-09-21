# run
pip install -r requirements.txt
python3 init_db.py
redis-server --port 5672
celery -A app.celery worker
flask run
