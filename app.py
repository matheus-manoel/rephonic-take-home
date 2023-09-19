from rephonic.factory import create_app, make_celery
from rephonic.api.routes import api

app = create_app()
celery = make_celery(app)
app.register_blueprint(api)

if __name__ == '__main__':
    app.run()
