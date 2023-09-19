from app import db  # import SQLAlchemy instance

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime)
    text_content = db.Column(db.String)
    author_name = db.Column(db.String)
