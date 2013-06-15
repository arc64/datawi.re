# unite!
import logging
from Queue import Queue as ThreadQueue
from threading import Thread

from datawire.core import app, db
from datawire.processing.queue import make_consumer

log = logging.getLogger(__name__)
pool_queue = ThreadQueue(maxsize=1)


def make_dispatcher(connection, queue, processor):
    def handle(body, message):
        pool_queue.put((processor, body, message), True)
        message.ack()
    make_consumer(connection, queue, handle)


def worker_target():
    while True:
        func, body, message = pool_queue.get(True)
        try:
            func(body, message)
        except Exception, e:
            log.exception(e)
        finally:
            pool_queue.task_done()
            db.session.close()


def create_pool():
    for i in range(app.config.get('PROCESSING_WORKERS')):
        t = Thread(target=worker_target)
        t.daemon = True
        t.name = 'Worker-%s' % i
        t.start()
