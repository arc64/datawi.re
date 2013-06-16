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
