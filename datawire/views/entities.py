from flask import Blueprint, request, url_for
from sqlalchemy.sql.functions import count

from datawire.core import db
from datawire.auth import require
from datawire.model import Entity, Facet, Match
from datawire.views.util import jsonify, obj_or_404
from datawire.views.pager import query_pager

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
    # select e.text, count(m.id) from entity e left join match m on m.entity_id = e.id group by e.text;
    q = Entity.all().filter_by(user_id=id)
    q = q.add_column(count(Match.id))
    q = q.outerjoin(Entity.matches)
    q = q.group_by(Entity)
    if 'facet' in request.args:
        q = q.filter(Entity.facet==request.args.get('facet'))
    def transform_result(result):
        entity_obj, count_ = result
        data = entity_obj.to_ref()
        data['count'] = count_
        return data
    return query_pager(q, 'entities.user_index', transform=transform_result, id=id)


@entities.route('/entities/<id>')
def get(id):
    require.logged_in()
    entity = obj_or_404(Entity.by_user_and_id(request.user, id))
    return jsonify(entity)


@entities.route('/entities', methods=['POST'])
def create():
    require.logged_in()
    entity = Entity.create(request.form, request.user)
    db.session.commit()
    return jsonify(entity)


@entities.route('/entities/<int:id>', methods=['POST'])
def update(id):
    require.logged_in()
    entity = obj_or_404(Entity.by_user_and_id(request.user, id))
    entity.update(request.form)
    db.session.commit()
    return jsonify(entity)


@entities.route('/entities/<int:id>', methods=['DELETE'])
def delete(id):
    require.logged_in()
    entity = obj_or_404(Entity.by_user_and_id(request.user, id))
    entity.delete()
    db.session.commit()
    return jsonify({'status': 'gone'}, status=410)
