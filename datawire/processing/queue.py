import logging
from kombu import Connection, Exchange, Queue
from datawire.core import app

log = logging.getLogger(__name__)

exchange = Exchange(app.config.get('INSTANCE', 'dwre'),
                    'topic', durable=True)

inbound_queue = Queue('inbound', exchange=exchange, routing_key='inbound.#')
matching_queue = Queue('matching', exchange=exchange, routing_key='matching.#')


def connect():
    return Connection(app.config.get('AMQP_QUEUE_URI'))


def make_consumer(connection, queue, callback):
    consumer = connection.Consumer([queue], callbacks=[callback])
    consumer.consume()
    log.info("Listening on: %s", queue)


def drain(connection):
    while True:
        connection.drain_events()


def publish(queue, routing_key, body):
    connection = Connection(app.config.get('AMQP_QUEUE_URI'))
    try:
        with connection.Producer(serializer='json') as producer:
            producer.publish(body,
                             exchange=exchange,
                             routing_key=routing_key,
                             declare=[queue])
    finally:
        connection.release()
