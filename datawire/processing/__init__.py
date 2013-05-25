from datawire.processing.queue import make_consumer, drain
from datawire.processing.queue import inbound_queue, matching_queue
from datawire.processing.inbound import handle_inbound
from datawire.processing.matching import handle_matching


def process():
    make_consumer(inbound_queue, handle_inbound)
    make_consumer(matching_queue, handle_matching)
    drain()
