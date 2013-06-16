import json
from anyjson import loads
from sqlalchemy.orm.query import Query
from datetime import datetime
from kombu.utils.encoding import bytes_t


class JSONEncoder(json.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    def __init__(self, refs=False):
        self.refs = refs
        super(JSONEncoder, self).__init__()

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Query):
            return list(obj)
        if self.refs and hasattr(obj, 'to_ref'):
            return obj.to_ref()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)


def queue_loads(obj):
    if isinstance(obj, bytes_t):
        obj = obj.decode()
    return loads(obj)
