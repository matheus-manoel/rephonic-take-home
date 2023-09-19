from app import app
from rephonic.extensions import db

with app.app_context():
    db.create_all()
