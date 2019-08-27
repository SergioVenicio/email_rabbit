from .connections import Connection


class LoggerQueue:
    def __init__(self):
        conn = Connection()
        self.connection = conn.connect()
        self.publisher_channel = self.connection.channel()

    def queue_declare(self):
        channel = self.connection.channel()
        channel.queue_declare(
            queue='logger', durable=True)

    def exchange_declare(self):
        channel = self.connection.channel()
        channel.exchange_declare(
            exchange='emails'
        )

    def get_connection(self):
        return self.connection
