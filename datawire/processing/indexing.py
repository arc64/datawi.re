import logging
from itertools import count

from datawire.core import db, elastic, elastic_index
from datawire.model import Match, Frame

log = logging.getLogger(__name__)


def index(frame_obj):
    data = frame_obj.to_ref()
    data['service'] = frame_obj.service.key
    data['event'] = frame_obj.event.key

    q = db.session.query(Match.entity_id)
    q = q.filter(Match.urn == frame_obj.urn)
    data['entities'] = [r[0] for r in q.distinct()]

    elastic.index(data, elastic_index, 'frame', frame_obj.urn)


def handle_indexing(body, message):
    routing_key = message.delivery_info.get('routing_key')
    log.info('%s - indexing: %s', routing_key, body['urn'])
    frame_obj = Frame.by_urn(body['urn'])
    index(frame_obj)


def reindex(step=5000):
    #elastic.indices.delete_index("datawire")
    q = Frame.all().order_by(Frame.submitted_at.desc())
    for offset in count(0, step):
        log.info("Re-indexing at %s", offset)
        if 0 == q.limit(step).offset(offset).count():
            return
        for frame_obj in q.limit(step).offset(offset):
            index(frame_obj)
