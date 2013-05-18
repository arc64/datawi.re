from boto.s3.connection import S3Connection
from boto.s3.connection import Location
from boto.s3.cors import CORSConfiguration
from boto.exception import S3ResponseError
from boto.s3.key import Key

from datawire.core import app
from datawire.store.common import Store


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
            cors_cfg = CORSConfiguration()
            cors_cfg.add_rule('GET', '*')
            self._bucket.set_cors(cors_cfg)
        return self._bucket

    def get_key(self, urn):
        parts = urn.split(':')[1:]
        key_name = '%s.json' % '/'.join(parts)
        key = Key(self.bucket, key_name)
        return key

    def _load(self, urn):
        try:
            key = self.get_key(urn)
            return key.get_contents_as_string()
        except S3ResponseError:
            return None

    def _store(self, urn, frame):
        key = self.get_key(urn)
        key.set_contents_from_string(frame, headers={
            'ETag': urn.split(':')[-1],
            'Content-Type': 'application/json',
            'Cache-Control': 'public; max-age=846000'
        })
        key.set_acl('public-read')
