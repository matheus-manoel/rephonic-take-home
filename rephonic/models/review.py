from rephonic.extensions import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    podcast_id = db.Column(db.String, nullable=False, index=True)
    created_date = db.Column(db.DateTime)
    text_content = db.Column(db.String)
    author_name = db.Column(db.String)

    def __init__(self, podcast_id, created_date, text_content, author_name):
        self.podcast_id = podcast_id
        self.created_date = created_date
        self.text_content = text_content
        self.author_name = author_name
