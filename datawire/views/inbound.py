from flask import Blueprint, request

from datawire.exc import BadRequest
from datawire.views.util import jsonify
from datawire.logic.inbound import handle_frame

inbound = Blueprint('inbound', __name__)


@inbound.route('/submit/<service_key>/<event_key>',
               methods=['PUT', 'POST'])
def submit(service_key, event_key):
    if request.json is None:
        raise BadRequest('Data must be submitted as JSON.')
    handle_frame(service_key, event_key, request.json)
    return jsonify({'status': 'ok'})
