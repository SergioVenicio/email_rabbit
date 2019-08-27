import os


class BaseConfig:
    DEBUG = True
    RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
    RABBIT_PORT = os.environ.get('RABBIT_PORT', 5672)
    RABBIT_USER = os.environ.get('RABBIT_USER', 'rabbitmq')
    RABBIT_PWD = os.environ.get('RABBIT_USER', 'rabbitmq')
    EMAIL_FROM = os.environ.get('EMAIL_FROM')
    EMAIL_SERVER = os.environ.get('EMAIL_SERVER')
    EMAIL_PWD = os.environ.get('EMAIL_SERVER')


class DevConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    DEBUG = False
