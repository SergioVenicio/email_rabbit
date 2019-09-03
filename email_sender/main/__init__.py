import os
import sys

sys.path.append("..")

from flask import Flask
from config import config

config = {
    'dev': config.DevConfig,
    'prod': config.ProdConfig
}


def create_app():
    app = Flask(__name__)

    with app.app_context():

        from main import views

        config_name = os.environ.get('APP_MODE', 'prod')

        app.config.from_object(config[config_name])

        app = initialize(app)

        return app


def initialize(app):
    from rabbitmq.queues import EmailsQueue

    email_queue = EmailsQueue()
    email_queue.queue_declare()
    email_queue.exchange_declare()
    app.email_queue = email_queue

    return app
