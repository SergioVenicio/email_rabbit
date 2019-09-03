from .connections import Connection


class BasicQueue():
    def __init__(self, exchange, queue, key):
        conn = Connection()

        self.exchange = exchange
        self.queue = queue
        self.key = key
        self.connection = conn.connect()
        self.pub_channel = self.connection.channel()
        self.cons_channel = self.connection.channel()

    def queue_declare(self, durable=True):
        self.pub_channel.queue_declare(
            queue=self.queue, durable=durable
        )

    def exchange_declare(self):
        self.pub_channel.exchange_declare(exchange=self.exchange)

    def queue_bind(self):
        self.pub_channel.queue_bind(
            exchange=self.exchange,
            queue=self.queue,
            routing_key=self.key
        )
    
    def publish_msg(self, body):
        self.pub_channel.basic_publish(
            exchange=self.exchange,
            routing_key=self.key,
            body=body
        )

    def start_consuming(self, callback, auto_ack=False):
        self.cons_channel.basic_consume(
            queue=self.queue,
            on_message_callback=callback,
            auto_ack=auto_ack
        )

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.cons_channel.start_consuming()
    
        

class LoggerQueue(BasicQueue):
    def __init__(self):
        super().__init__('emails', 'logger', 'logger')


class EmailsQueue(BasicQueue):
    def __init__(self):
        super().__init__('emails', 'email', 'emails')