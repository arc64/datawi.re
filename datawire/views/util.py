from datetime import datetime
from flask import Response, request, url_for
from sqlalchemy.orm.query import Query
import json

from datawire.exc import NotFound

BOOL_TRUISH = ['true', '1', 'yes', 'y', 't']


def obj_or_404(obj):
    if obj is None:
        NotFound()
    return obj


def arg_bool(name, default=False):
    v = request.args.get(name, '')
    if not len(v):
        return default
    return v in BOOL_TRUISH


def arg_int(name, default=None):
    try:
        v = request.args.get(name)
        return int(v)
    except (ValueError, TypeError):
        return default


def get_limit(default=50):
    return max(0, min(1000, arg_int('limit', default=default)))


def get_offset(default=0):
    return max(0, arg_int('offset', default=default))


def query_pager(q, route, data=None, transform=None, **kw):
    data = data or {}
    count = q.count()
    limit = get_limit()
    offset = get_offset()
    prev_offset = max(offset - limit, 0)
    prev = None if offset == 0 else \
        url_for(route, limit=limit, offset=prev_offset, _external=True, **kw)
    has_next = count < (offset + limit)
    next_offset = min(limit + offset, count)
    next = None if has_next else \
        url_for(route, limit=limit, offset=next_offset, _external=True, **kw)
    results = q.limit(limit).offset(offset)
    if transform is not None:
        results = [transform(r) for r in results]
    data.update({
        'count': count,
        'limit': limit,
        'offset': offset,
        'previous': prev,
        'next': next,
        'results': results
    })
    return jsonify(data, refs=True)


class JSONEncoder(json.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    def __init__(self, refs=False):
        self.refs = refs
        super(JSONEncoder, self).__init__()

    def encode(self, obj):
        return super(JSONEncoder, self).encode(obj)

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Query):
            return list(obj)
        if self.refs and hasattr(obj, 'to_ref'):
            return obj.to_ref()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        raise TypeError("%r is not JSON serializable" % obj)


def jsonify(obj, status=200, headers=None, refs=False):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    data = JSONEncoder(refs=refs).encode(obj)
    if 'callback' in request.args:
        cb = request.args.get('callback')
        data = '%s && %s(%s)' % (cb, cb, data)
    return Response(data, headers=headers,
                    status=status, mimetype='application/json')
