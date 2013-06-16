from flask import Blueprint, request, url_for
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import or_, func
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
    q = Entity.all().filter_by(user_id=id)
    count_field = count(func.distinct(Match.id))
    q = q.add_column(count_field)
    q = q.outerjoin(Entity.matches)
    q = q.group_by(Entity)
    if 'category' in request.args:
        q = q.filter(Entity.category == request.args.get('category'))

    if 'entity' in request.args:
        q = q.outerjoin(Match.frame)
        other_match = aliased(Match)
        q = q.outerjoin(other_match, Frame.urn == other_match.urn)
        fq = or_(other_match.entity_id.in_(request.args.get('entity')),
                 other_match.entity_id == None)
        q = q.filter(fq)

    q = q.order_by(count_field.desc())
    q = q.order_by(Entity.text.asc())

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
