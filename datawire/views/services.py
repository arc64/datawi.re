from flask import Blueprint, request, url_for

from datawire.auth import require
from datawire.model import Service
from datawire.views.util import jsonify, obj_or_404
from datawire.views.pager import query_pager

services = Blueprint('services', __name__)


@services.route('/services')
def index():
    q = Service.all()
    return query_pager(q, 'services.index')


@services.route('/services/<key>')
def get(key):
    service = obj_or_404(Service.by_key(key))
    require.service.view(service)
    return jsonify(service)
