from flask import Blueprint, request, url_for
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.functions import count

from datawire.auth import require
from datawire.model import Service, Frame, Match, Entity
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


@frames.route('/users/<int:id>/feed')
def user_index(id):
    require.user_id(id)
    q = Frame.all()
    q = q.join(Frame.matches)
    q = q.join(Match.entity)
    q = q.filter(Entity.user_id == id)
    entities = request.args.getlist('entity')
    if len(entities):
        q = q.group_by(Frame)
        q = q.filter(Entity.id.in_(entities))
        q = q.having(count(Entity.id) == len(entities))
    q = q.order_by(Frame.created_at.desc())
    return query_pager(q, 'frames.user_index', id=id)


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
