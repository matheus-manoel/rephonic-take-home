from flask import Flask
from .extensions import db, celery

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'

    db.init_app(app)

    #app.config.from_object('rephonic.celery_config')
    app.config['broker_url'] = 'redis://localhost:5672/0'
    app.config['result_backend'] = 'redis://localhost:5672/0'
    celery.conf.update(app.config)
    print(app.config)
    
    return app

def make_celery(app):
    celery.conf.update(app.config)
    return celery

