import sys

sys.path.append("..")

import pika
import json

from datetime import datetime

from sender import Email
from rabbitmq.queues import EmailsQueue, LoggerQueue

email = Email()

email_queue = EmailsQueue()
email_queue.exchange_declare()
email_queue.queue_declare()
email_queue.queue_bind()

logger_queue = LoggerQueue()
logger_queue.queue_declare()
logger_queue.queue_bind()


def send_email(ch, method, properties, msg):
    print(msg)
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

        logger_queue.publish_msg(body=log)

        print(log)
    else:

        log = '[ERROR][{0}] Email send to {1}.'.format(time, _to)

        logger_queue.publish_msg(body=log)
        # fila de erro <- Tratar o erro
        # ch.basic_ack(method.delivery_tag)

        print(log)

email_queue.start_consuming(callback=send_email)
