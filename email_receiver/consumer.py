import pika
import json

from datetime import datetime

from sender import Email
from rabbitmq.queues import EmailsQueue, LoggerQueue

email = Email()

email_queue = EmailsQueue()
email_queue.exchange_declare()
email_queue.queue_declare()
channel = email_queue.get_connection().channel()
channel.queue_bind(exchange='emails', queue='email', routing_key='emails')

logger_queue = LoggerQueue()
logger_queue.queue_declare()
logger_channel = logger_queue.get_connection().channel()
logger_channel.exchange_declare(exchange='emails')
logger_channel.queue_declare(queue='logger', durable=True)


def send_email(ch, method, properties, msg):
    json_msg = json.loads(msg)

    _to = json_msg['email']

    resp = email.sendemail(
        to=_to,
        subject=json_msg['subject'],
        msg=json_msg['msg'],
    )

    resp = {}

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not resp:

        ch.basic_ack(method.delivery_tag)

        log = '[SUCCESS][{0}] Email send to {1}.'.format(time, _to)

        logger_channel.basic_publish(
            exchange='emails', routing_key='logger', body=log
        )

        print(log)
    else:

        log = '[ERROR][{0}] Email send to {1}.'.format(time, _to)

        logger_channel.basic_publish(
            exchange='emails', routing_key='logger', body=log
        )
        # fila de erro <- Tratar o erro
        # ch.basic_ack(method.delivery_tag)

        print(log)


channel.basic_consume(
    queue='email', on_message_callback=send_email, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
