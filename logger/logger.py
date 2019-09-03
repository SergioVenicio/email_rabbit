import sys

sys.path.append("..")

from pymongo import MongoClient

from rabbitmq.queues import LoggerQueue

# Mongo
client = MongoClient('mongodb://localhost:27017/')

logger_db = client['logger']
logger_coll = logger_db['logs']

queue = LoggerQueue()
queue.exchange_declare()
queue.queue_declare()
queue.queue_bind()

def save_log(ch, method, properties, msg):
    resp = logger_coll.insert_one({
        'msg': str(msg)
    })

    ch.basic_ack(method.delivery_tag)

queue.start_consuming(callback=save_log)