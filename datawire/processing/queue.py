import logging
from kombu import Connection, Exchange, Queue
from datawire.core import app

log = logging.getLogger(__name__)

exchange = Exchange(app.config.get('INSTANCE', 'dwre'),
                    'topic', durable=True)

inbound_queue = Queue('inbound', exchange=exchange, routing_key='inbound.#')


def connect():
    return Connection(app.config.get('AMQP_QUEUE_URI'))


def handle_message(body, message):
    queue, service_key, event_key = message.delivery_info.get('routing_key').split('.')
    log.info('%s - received: %s / %s', queue, service_key, event_key)
    from pprint import pprint
    pprint(body)
    message.ack()
    print message.delivery_info


def process():
    conn = connect()
    with conn.Consumer([inbound_queue], callbacks=[handle_message]):
        while True:
            conn.drain_events()


def publish(queue, routing_key, body):
    conn = connect()
    with conn.Producer(serializer='json') as producer:
        producer.publish(body,
                         exchange=exchange,
                         routing_key=routing_key,
                         declare=[queue])
