from datawire.processing.queue import inbound_queue, process_queue
from datawire.processing.inbound import handle_inbound

def process():
    process_queue(inbound_queue, handle_inbound)
