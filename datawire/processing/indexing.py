import logging
from itertools import count

from datawire.core import db, elastic, elastic_index
from datawire.model import Match, Frame
#from datawire.store import load_frame

log = logging.getLogger(__name__)


def index(frame_obj):
    #frame = load_frame(frame_urn)
    #del frame['data']
    data = frame_obj.to_ref()
    data['service'] = frame_obj.service.key
    data['event'] = frame_obj.event.key

    q = db.session.query(Match.entity_id)
    q = q.filter(Match.urn == frame_obj.urn)
    data['entities'] = [eid for (eid,) in q.distinct()]
    elastic.index(data, elastic_index, 'frame', frame_obj.urn)


def handle_matching(body, message):
    routing_key = message.delivery_info.get('routing_key')
    log.info('%s - indexing: %s', routing_key, body['urn'])
    index(body['urn'])


def reindex(step=5000):
    q = Frame.all().order_by(Frame.submitted_at.desc())
    for offset in count(0, step):
        log.info("Re-indexing at %s", offset)
        if 0 == q.limit(step).offset(offset).count():
            return
        for frame_obj in q.limit(step).offset(offset):
            index(frame_obj)
