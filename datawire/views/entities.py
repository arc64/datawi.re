from flask import Blueprint, request, url_for

from datawire.core import db
from datawire.auth import require
from datawire.model import Entity, Facet
from datawire.views.util import jsonify, obj_or_404
from datawire.views.util import query_pager

entities = Blueprint('entities', __name__)


@entities.route('/facets')
def facet_index():
    facets = Facet.all()
    return jsonify({
        'results': facets,
        'count': len(facets)
    })


@entities.route('/facets/<key>')
def facet_get(key):
    facet = obj_or_404(Facet.by_key(key))
    return jsonify(facet)


@entities.route('/users/<int:id>/entities')
def user_index(id):
    require.user_id(id)
    q = Entity.all().filter_by(user_id=id)
    if 'facet' in request.args:
        q = q.filter_by(facet=request.args.get('facet'))
    return query_pager(q, 'entities.user_index')


@entities.route('/entities/<id>')
def get(id):
    require.logged_in()
    entity = Entity.all().filter_by(id=id).filter_by(user=request.user)
    entity = obj_or_404(entity.first())
    return jsonify(entity)


@entities.route('/entities', methods=['POST'])
def create():
    require.logged_in()
    entity = Entity.create(request.form, request.user)
    db.session.commit()
    return jsonify(entity)


@entities.route('/entities/<int:id>', methods=['POST'])
def update():
    require.logged_in()
    entity = Entity.all().filter_by(id=id).filter_by(user=request.user)
    entity = obj_or_404(entity.first())
    entity.update(request.form)
    db.session.commit()
    return jsonify(entity)
