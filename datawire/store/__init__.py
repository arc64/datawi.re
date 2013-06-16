from urlparse import urlparse

from datawire.core import app
from datawire.store.file import FileStore
from datawire.store.s3 import S3Store

STORES = {
    'file': FileStore,
    's3': S3Store
}


def get_backend(instance={'_': None}):
    if instance['_'] is None:
        parsed = urlparse(app.config.get('STORE_URL'))
        instance['_'] = STORES.get(parsed.scheme)(parsed)
    return instance['_']


def store_frame(frame):
    return get_backend().store(frame)


def load_frame(urn):
    # TODO: Memcache a few things (10k?)
    return get_backend().load(urn)


def frame_url(urn):
    return get_backend().frame_url(urn)
