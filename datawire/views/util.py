from datetime import datetime
from flask import Response, request
import json


class JSONEncoder(json.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    def encode(self, obj):
        if hasattr(obj, 'to_dict'):
            obj = obj.to_dict()
        return super(JSONEncoder, self).encode(obj)

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        raise TypeError("%r is not JSON serializable" % obj)


def jsonify(obj, status=200, headers=None):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    data = json.dumps(obj, cls=JSONEncoder)
    if 'callback' in request.args:
        cb = request.args.get('callback')
        data = '%s && %s(%s)' % (cb, cb, data)
    return Response(data, headers=headers,
                    status=status, mimetype='application/json')
