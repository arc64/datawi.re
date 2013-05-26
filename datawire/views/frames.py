from flask import Blueprint, request, url_for

from datawire.auth import require
from datawire.model import Service, Frame
from datawire.exc import BadRequest, NotFound
from datawire.store import load_frame, frame_url
from datawire.views.util import jsonify, arg_bool, obj_or_404
from datawire.views.pager import query_pager
from datawire.processing.inbound import generate_frame
from datawire.processing.queue import publish, inbound_queue

frames = Blueprint('frames', __name__)


def frameset(q, route, data=None):
    # TODO: add argument for RSS support.
    data = data or {}
    q = q.order_by(Frame.created_at.desc())
    return query_pager(q, route, data=data)


@frames.route('/frames')
def index():
    q = Frame.all()
    return frameset(q, 'frames.index')


@frames.route('/frames/<urn>')
def get(urn):
    # TODO: authz checks.
    data = load_frame(urn)
    if data is None:
        raise NotFound('Frame: %s' % urn)
    headers = {
        'X-Backend-Location': frame_url(urn),
        'ETag': data['hash'],
        'Cache-Control': 'public; max-age: 8460000'
    }
    return jsonify(data, headers=headers)


@frames.route('/frames/<service_key>/<event_key>',
              methods=['PUT', 'POST'])
def submit(service_key, event_key):
    if request.json is None:
        raise BadRequest('Data must be submitted as JSON.')

    service = obj_or_404(Service.by_key(service_key))
    require.service.publish(service)

    if arg_bool('sync'):
        urn = generate_frame(service_key, event_key, request.json)
        return jsonify({'status': 'ok', 'urn': urn})
    else:
        routing_key = 'inbound.%s.%s' % (service_key, event_key)
        publish(inbound_queue, routing_key, request.json)
        return jsonify({'status': 'queued'})
