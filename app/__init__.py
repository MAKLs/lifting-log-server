"""
Configure the Flask application and initialize its database
"""
from flask import Flask
from .models import db
from .blueprints.api.views import api

def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(configuration)
    app.register_blueprint(api, url_prefix='/{}'.format(api.name))
    db.init_app(app)
    init_db(app)
    return app


def init_db(app):
    with app.app_context():
        db.create_all()