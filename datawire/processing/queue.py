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


def process_queue(queue, callback):
    conn = connect()
    log.info("Listening on: %s", queue)
    with conn.Consumer([queue], callbacks=[callback]):
        while True:
            conn.drain_events()


def publish(queue, routing_key, body):
    conn = connect()
    with conn.Producer(serializer='json') as producer:
        producer.publish(body,
                         exchange=exchange,
                         routing_key=routing_key,
                         declare=[queue])
