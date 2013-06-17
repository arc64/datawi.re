from flask import Blueprint, request, url_for
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import or_, and_, func
from sqlalchemy.orm import aliased

from datawire.core import db
from datawire.auth import require
from datawire.model import Entity, Category, Match, Frame
from datawire.processing.queue import publish, entity_queue
from datawire.views.util import jsonify, obj_or_404
from datawire.views.pager import query_pager

entities = Blueprint('entities', __name__)


@entities.route('/categories')
def category_index():
    categories = Category.all()
    return jsonify({
        'results': categories,
        'count': len(categories)
    })


@entities.route('/categories/<key>')
def category_get(key):
    category = obj_or_404(Category.by_key(key))
    return jsonify(category)


@entities.route('/users/<int:id>/entities')
def user_index(id):
    require.user_id(id)
    q = Entity.all()
    q = q.join(Entity.matches)
    q = q.join(Match.frame)
    other_match = aliased(Match)
    q = q.join(other_match, Frame.urn == other_match.urn)
    other_entity = aliased(Entity)
    q = q.join(other_entity, other_match.entity_id == other_entity.id)

    q = q.filter(Entity.user_id == id)
    q = q.filter(or_(other_entity.user_id == id, other_entity.user_id == None))

    if 'category' in request.args:
        q = q.filter(Entity.category == request.args.get('category'))

    if 'entity' in request.args:
        entities = request.args.getlist('entity')
        fq = or_(other_match.entity_id.in_(entities),
                 other_match.entity_id == None)
        q = q.filter(fq)

    q = q.group_by(Entity)
    count_field = count(func.distinct(Match.urn))
    q = q.add_column(count_field)
    q = q.order_by(Entity.text.asc())

    print q

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
    publish(entity_queue, 'entity.create', entity)
    return jsonify(entity)


@entities.route('/entities/<int:id>', methods=['POST'])
def update(id):
    require.logged_in()
    entity = obj_or_404(Entity.by_user_and_id(request.user, id))
    data = {'old': entity.to_dict()}
    entity.update(request.form)
    db.session.commit()
    data['new'] = entity
    publish(entity_queue, 'entity.update', data)
    return jsonify(entity)


@entities.route('/entities/<int:id>', methods=['DELETE'])
def delete(id):
    require.logged_in()
    entity = obj_or_404(Entity.by_user_and_id(request.user, id))
    publish(entity_queue, 'entity.delete', entity)
    entity.delete()
    db.session.commit()
    return jsonify({'status': 'gone'}, status=410)
