import re
import logging

from datawire.core import db
from datawire.model import Entity, Match

log = logging.getLogger(__name__)


class Matcher(object):

    def __init__(self, entity):
        self.pattern = re.compile(entity.text, re.I | re.M)

    def __call__(self, value):
        match = self.pattern.search(unicode(value))
        return match is not None

    def __hash__(self):
        return hash(self.pattern)


def itervalues(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            for ik, iv in itervalues(v, path + '.' + k):
                yield ik, iv
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            for ik, iv in itervalues(v, path + '[' + i + ']'):
                yield ik, iv
    else:
        yield path, obj


def match(frame):
    entities = Entity.all()
    filters = [(Matcher(e), e) for e in entities]
    for k, v in itervalues(frame.get('data'), 'data'):
        for matcher, entity in filters:
            if matcher(v) and not Match.exists(frame['urn'], entity):
                field = k.split('.', 1).pop()
                match = Match.create(frame['urn'], field, entity)
                log.info("match: %s", match)
                db.session.flush()
                #print 'User "%s" will be notified, as %s matches for "%s" on field %s' % (
                #    entity.user.name, frame['urn'], entity.text, field
                #    )
    db.session.commit()


def handle_matching(body, message):
    try:
        routing_key = message.delivery_info.get('routing_key')
        log.info('%s - received: %s', routing_key, body['urn'])
        match(body)
    except Exception, e:
        log.exception(e)
    finally:
        message.ack()
