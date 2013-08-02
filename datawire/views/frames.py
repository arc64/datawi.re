from flask import Blueprint, request, url_for
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.functions import count
from sqlalchemy.orm import aliased

from datawire.core import elastic, elastic_index
from datawire.auth import require
from datawire.model import Service, Frame, Match, Entity
from datawire.exc import BadRequest, NotFound
from datawire.store import load_frame, frame_url
from datawire.views.util import jsonify, arg_bool, obj_or_404
from datawire.views.util import get_limit, get_offset
from datawire.views.pager import query_pager
from datawire.processing.inbound import generate_frame
from datawire.processing.queue import publish, inbound_queue

frames = Blueprint('frames', __name__)


@frames.route('/frames')
def index():
    q = Frame.all()
    q = q.order_by(Frame.action_at.desc())
    return query_pager(q, 'frames.index')


@frames.route('/users/<int:id>/feed')
def user_index(id):
    require.user_id(id)

    esq = {
        "query": {
            "filtered": {
                "query": {"match_all": {}}, "filter": {}
            }
        },
        "sort": [{"action_at": {"order": "desc"}}],
        "size": get_limit(),
        "from": get_offset(),
        "facets": {"entities": {
            "terms": {"field": "entities"}}
        }
    }

    filters = request.args.getlist('entity')
    if len(filters):
        esq['query']['filtered']['filter']['and'] = []
        for entity_id in filters:
            fq = {"term": {"entities": entity_id}}
            esq['query']['filtered']['filter']['and'].append(fq)
    else:
        esq['query']['filtered']['filter']['or'] = []
        for entity in Entity.all().filter(Entity.user_id == id):
            fq = {"term": {"entities": entity.id}}
            esq['query']['filtered']['filter']['or'].append(fq)

    res = elastic.search_raw(esq, elastic_index, 'frame')
    frame_urns = [r['_id'] for r in res['hits']['hits']]
    q = Frame.all().filter(Frame.urn.in_(frame_urns))
    frames = dict([(f.urn, f) for f in q])
    frames = [frames.get(urn) for urn in frame_urns]
    return query_pager(frames, 'frames.user_index',
                       count=res['hits']['total'],
                       paginate=False,
                       id=id)


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

    data = {
        'body': request.json,
        'headers': dict(request.headers.items())
    }

    if arg_bool('sync'):
        urn = generate_frame(service_key, event_key, data)
        return jsonify({'status': 'ok', 'urn': urn})
    else:
        routing_key = 'inbound.%s.%s' % (service_key, event_key)
        publish(inbound_queue, routing_key, data)
        return jsonify({'status': 'queued'})
