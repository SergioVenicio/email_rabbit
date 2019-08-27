from flask import current_app as app
import pika


class Connection:
    def __init__(self):
        self.host = app.config['RABBIT_HOST']
        self.port = app.config['RABBIT_PORT']
        self.username = app.config['RABBIT_USER']
        self.pwd = app.config['RABBIT_PWD']

    def connect(self):
        credentials = pika.PlainCredentials(
            username=self.username,
            password=self.pwd
        )
        conn_params = pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host='/',
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters=conn_params)
        return connection
