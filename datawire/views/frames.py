from flask import Blueprint, request

from datawire.exc import BadRequest, NotFound
from datawire.store import load_frame, frame_url
from datawire.views.util import jsonify
from datawire.logic.inbound import generate_frame

frames = Blueprint('frames', __name__)


@frames.route('/submit/<service_key>/<event_key>',
              methods=['PUT', 'POST'])
def submit(service_key, event_key):
    if request.json is None:
        raise BadRequest('Data must be submitted as JSON.')
    generate_frame(service_key, event_key, request.json)
    return jsonify({'status': 'ok'})


@frames.route('/frames/<urn>')
def get(urn):
    # TODO: Cache headers.
    data = load_frame(urn)
    if data is None:
        raise NotFound('Frame: %s' % urn)
    headers = {'X-Backend-Location': frame_url(urn)}
    return jsonify(data, headers=headers)
