from pprint import pprint
from datetime import datetime

from datawire.exc import NotFound
from datawire.model import Service, Event, Frame
from datawire.model.util import make_token, data_hash


def handle_frame(service_key, event_key, data):
    service = Service.by_key(service_key)
    if service is None:
        raise NotFound('No such service: %s' % service_key)
    event = Event.by_key(service, event_key)
    if event is None:
        raise NotFound('No such event: %s' % event_key)

    frame = {
        'id': make_token(),
        'service': service_key,
        'event': event_key,
        'hash': data_hash(data),
        'created_at': datetime.utcnow(),
        'data': data
    }
    frame['urn'] = Frame.to_urn(frame)

    pprint(frame)
