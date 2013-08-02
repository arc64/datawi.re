from datawire.processing.queue import drain, connect
from datawire.processing.queue import inbound_queue, matching_queue, entity_queue, indexing_queue
from datawire.processing.inbound import handle_inbound
from datawire.processing.matching import handle_matching
from datawire.processing.indexing import handle_indexing
from datawire.processing.entity import handle_entity
from datawire.processing.workers import make_dispatcher, create_pool


def process():
    create_pool()
    connection = connect()
    make_dispatcher(connection, inbound_queue, handle_inbound)
    make_dispatcher(connection, matching_queue, handle_matching)
    make_dispatcher(connection, entity_queue, handle_entity)
    make_dispatcher(connection, indexing_queue, handle_indexing)
    drain(connection)
