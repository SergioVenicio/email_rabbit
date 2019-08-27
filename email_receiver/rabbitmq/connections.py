import os
import pika


class Connection:
    def __init__(self):
        self.host = os.environ.get('RABBIT_HOST')
        self.port = os.environ.get('RABBIT_PORT')
        self.username = os.environ.get('RABBIT_USER')
        self.pwd = os.environ.get('RABBIT_PWD')

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
