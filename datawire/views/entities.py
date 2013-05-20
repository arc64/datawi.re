from flask import Blueprint, request, url_for

from datawire.auth import require
from datawire.model import Entity
from datawire.views.util import jsonify, obj_or_404
from datawire.views.util import query_pager

entities = Blueprint('entities', __name__)


@entities.route('/users/<int:id>/entities')
def user_index(id):
    require.user_id(id)
    q = Entity.all().filter_by(user_id=id)
    return query_pager(q, 'entities.user_index')


@entities.route('/entities/<id>')
def get(id):
    require.logged_in()
    entity = Entity.all().filter_by(id=id).filter_by(user=request.user)
    entity = obj_or_404(entity.first())
    return jsonify(entity)
