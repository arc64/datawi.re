import json

from datawire.views.util import JSONEncoder


class Store(object):

    def __init__(self, url):
        self.url = url

    def store(self, frame):
        urn = frame.get('urn')
        data = json.dumps(frame, cls=JSONEncoder)
        return self._store(urn, data)

    def load(self, urn):
        data = self._load(urn)
        if data is not None:
            data = json.loads(data)
        return data
