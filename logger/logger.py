from pymongo import MongoClient

from rabbitmq.queues import LoggerQueue

# Mongo
client = MongoClient('mongodb://localhost:27017/')

logger_db = client['logger']
logger_coll = logger_db['logs']

queue = LoggerQueue()
queue.queue_declare()
channel = queue.get_connection().channel()
channel.exchange_declare(exchange='emails')
channel.queue_declare(queue='emails', durable=True)


def save_log(ch, method, properties, msg):
    logger_coll.insert_one({
        'msg': str(msg)
    })

    ch.basic_ack(method.delivery_tag)


channel.basic_consume(
    queue='logger', on_message_callback=save_log, auto_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()