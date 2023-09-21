from flask_migrate import Migrate
from flask import Flask
from .extensions import db, celery
from rephonic.api.routes import api

def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
    
    if config:
        app.config.from_object(config)

    db.init_app(app)
    Migrate(app, db)

    app.config['broker_url'] = 'redis://localhost:5672/0'
    app.config['result_backend'] = 'redis://localhost:5672/0'
    app.config['broker_connection_retry_on_startup'] = True
    celery.conf.update(app.config)

    app.register_blueprint(api)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    
    return app

def make_celery(app):
    celery.conf.update(app.config)
    return celery

