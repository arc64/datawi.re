import os

from datawire.store.common import Store


class FileStore(Store):

    def urn_path(self, urn):
        if not os.path.isdir(self.url.path):
            os.makedirs(self.url.path)
        return os.path.join(self.url.path, '%s.json' % urn)

    def _load(self, urn):
        path = self.urn_path(urn)
        if not os.path.isfile(path):
            return None
        with open(path, 'rb') as fh:
            return fh.read()

    def _store(self, urn, frame):
        path = self.urn_path(urn)
        with open(path, 'wb') as fh:
            fh.write(frame)
