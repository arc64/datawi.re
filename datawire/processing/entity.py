import logging
from collections import defaultdict

from datawire.model import Entity

log = logging.getLogger(__name__)


def get_filters():
    # TODO: one day, this will live in memory.
    filters = defaultdict(list)
    for entity in Entity.all():
        filters[entity.pattern].append(entity.id)
    return filters.items()


def handle_entity(body, message):
    from datawire.processing.matching import backsearch
    queue, operation = message.delivery_info.get('routing_key').split('.')
    log.info('%s - %s', queue, operation)
    if operation == 'create':
        entity = Entity.by_id(body.get('id'))
        backsearch(entity)
