import logging

from datawire.core import db
from datawire.model import Match, Frame
from datawire.model.util import itervalues
from datawire.store import load_frame
from datawire.processing.entity import get_filters

log = logging.getLogger(__name__)

BACKSEARCH_LIMIT = 100000
BACKSEARCH_FIND = 15


def match(frame, pattern, entity_ids):
    matches = []
    for k, v in itervalues(frame.get('data'), 'data'):
        rem = pattern.search(unicode(v))
        if rem is None:
            continue
        for entity_id in entity_ids:
            if not Match.exists(frame['urn'], entity_id):
                field = k.split('.', 1).pop()
                match = Match.create(frame['urn'], field, entity_id)
                log.info("match: %s", match)
                matches.append(match)
    return matches


def match_frame(frame):
    filters = get_filters()
    for pattern, entity_ids in filters:
        match(frame, pattern, entity_ids)
    db.session.commit()


def handle_matching(body, message):
    routing_key = message.delivery_info.get('routing_key')
    log.info('%s - received: %s', routing_key, body['urn'])
    match_frame(body)


def backsearch(entity, step=5000):
    found_count = 0
    pattern = entity.pattern
    q = Frame.all().order_by(Frame.submitted_at.desc())
    for offset in range(0, BACKSEARCH_LIMIT, step):
        log.info("Backsearch [%s] at %s (found: %s)", entity.text, offset, found_count)
        if 0 == q.limit(step).offset(offset).count():
            return
        for frame_obj in q.limit(step).offset(offset):
            frame = load_frame(frame_obj.urn)
            matches = match(frame, pattern, [entity.id])
            found_count += len(matches)
            if len(matches):
                db.session.commit()
            if found_count >= BACKSEARCH_FIND:
                return
