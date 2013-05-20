from flask import Blueprint, request, url_for

from datawire.auth import require
from datawire.model import Service, Event
from datawire.views.util import jsonify, obj_or_404
from datawire.views.util import get_limit, get_offset

events = Blueprint('events', __name__)


@events.route('/services/<service_key>/events')
def index(service_key):
    service = obj_or_404(Service.by_key(service_key))
    require.service.view(service)
    q = Event.all().filter_by(service=service)
    result = {'count': q.count()}
    q = q.limit(get_limit())
    q = q.offset(get_offset())
    result['results'] = q
    return jsonify(result, refs=True)


@events.route('/services/<service_key>/events/<event_key>')
def get(service_key, event_key):
    service = obj_or_404(Service.by_key(service_key))
    require.service.view(service)
    event = obj_or_404(service.events.filter_by(key=event_key).first())
    return jsonify(event)
