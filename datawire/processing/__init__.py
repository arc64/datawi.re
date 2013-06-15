from datawire.processing.queue import drain, connect
from datawire.processing.queue import inbound_queue, matching_queue
from datawire.processing.inbound import handle_inbound
from datawire.processing.matching import handle_matching
from datawire.processing.workers import make_dispatcher, create_pool


def process():
    create_pool()
    connection = connect()
    make_dispatcher(connection, inbound_queue, handle_inbound)
    make_dispatcher(connection, matching_queue, handle_matching)
    drain(connection)
