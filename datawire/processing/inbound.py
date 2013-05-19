from pprint import pprint
from datetime import datetime

from datawire.exc import NotFound, BadRequest
from datawire.core import db
from datawire.model import Service, Event, Frame
from datawire.model.util import data_hash
from datawire.store import store_frame
from datawire.processing.queue import inbound_queue, publish


def generate_frame_async(service_key, event_key, data):
    routing_key = 'inbound.%s.%s' % (service_key, event_key)
    publish(inbound_queue, routing_key, data)


def generate_frame(service_key, event_key, data):
    service = Service.by_key(service_key)
    if service is None:
        raise NotFound('No such service: %s' % service_key)
    event = Event.by_key(service, event_key)
    if event is None:
        raise NotFound('No such event: %s' % event_key)

    frame = {
        'service': service_key,
        'event': event_key,
        'data': data
    }
    frame.update({
        'hash': data_hash(frame),
        'created_at': datetime.utcnow()
    })
    frame['urn'] = Frame.to_urn(frame)

    if Frame.by_hash(frame['hash']) is not None:
        raise BadRequest('Duplicate content, hash: %(hash)s' % frame)

    Frame.create(service, frame)
    store_frame(frame)
    db.session.commit()

    # TODO: actually queue this :)
    pprint(frame)
