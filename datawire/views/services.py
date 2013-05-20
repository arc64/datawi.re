from flask import Blueprint, request, url_for

from datawire.auth import require
from datawire.model import Service
from datawire.views.util import jsonify, obj_or_404
from datawire.views.util import get_limit, get_offset

services = Blueprint('services', __name__)


@services.route('/services')
def index():
    q = Service.all()
    result = {'count': q.count()}
    q = q.limit(get_limit())
    q = q.offset(get_offset())
    result['results'] = q
    return jsonify(result)


@services.route('/services/<key>')
def get(key):
    service = obj_or_404(Service.by_key(key))
    require.service.publish(service)
    return jsonify(service)
