import logging
from datetime import datetime

from datawire.exc import NotFound, BadRequest
from datawire.core import db
from datawire.model import Service, Event, Frame
from datawire.model.util import data_hash
from datawire.store import store_frame
from datawire.processing.queue import publish, matching_queue
from datawire.processing.util import parse_datetime, parse_url

log = logging.getLogger(__name__)


def handle_inbound(body, message):
    queue, service_key, event_key = message.delivery_info.get('routing_key').split('.')
    log.info('%s - received: %s / %s', queue, service_key, event_key)
    generate_frame(service_key, event_key, body)


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
        'data': data.get('body')
    }
    headers = data.get('headers')
    frame.update({
        'source_url': parse_url(headers.get('X-Source-Location')),
        'details_url': parse_url(headers.get('X-Details-Location')),
        'hash': data_hash(frame),
        'action_at': parse_datetime(headers.get('X-Action-Time')),
        'submitted_at': datetime.utcnow()
    })

    if not frame['action_at']:
        frame['action_at'] = frame['submitted_at']
    else:
        frame['action_at'] = min(frame['action_at'], frame['submitted_at'])

    frame['urn'] = Frame.to_urn(frame)

    if Frame.by_hash(frame['hash']) is not None:
        raise BadRequest('Duplicate content, hash: %(hash)s' % frame)

    Frame.create(service, event, frame)
    store_frame(frame)
    db.session.commit()

    log.info("created: %(urn)s (%(hash)s)", frame)
    routing_key = 'matching.%s.%s' % (service_key, event_key)
    publish(matching_queue, routing_key, frame)
    return frame['urn']
