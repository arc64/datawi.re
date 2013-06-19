import logging

from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.cors import CORSConfiguration
from boto.exception import S3ResponseError
from boto.s3.key import Key

from datawire.core import app
from datawire.store.common import Store

log = logging.getLogger(__name__)


class S3Store(Store):

    @property
    def bucket(self):
        if not hasattr(self, '_conn'):
            self._conn = S3Connection(app.config.get('S3_ACCESS_KEY'),
                                      app.config.get('S3_SECRET_KEY'))
            self._bucket = self._conn.lookup(self.url.hostname)
            if self._bucket is None:
                self._bucket = self._conn.create_bucket(self.url.hostname,
                                                        location=Location.EU)
            self._bucket.set_acl('public-read')
        return self._bucket

    def get_key(self, urn):
        parts = urn.split(':')[2:]
        key_name = '%s.json' % '/'.join(parts)
        key = Key(self.bucket, key_name)
        return key

    def _load(self, urn):
        try:
            key = self.get_key(urn)
            return key.get_contents_as_string()
        except S3ResponseError:
            log.info("Key not found: %s", urn)
            return None

    def _store(self, urn, frame):
        key = self.get_key(urn)
        key.set_contents_from_string(frame, headers={
            'ETag': urn.split(':')[-1],
            'Content-Type': 'application/json',
            'Cache-Control': 'public; max-age=846000'
        })
        key.set_acl('public-read')

    def frame_url(self, urn):
        parts = urn.split(':')[2:]
        if app.get('ENABLE_FRAMETHROWER'):
            return 'http://ft-%s.%s/%s' % (parts[-1][:1], self.url.hostname, urn)
        key = '%s.json' % '/'.join(parts)
        return 'http://%s/%s' % (self.url.hostname, key)
