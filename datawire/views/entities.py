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
    #res = cls.es.conn.search_raw(q, cls.es.index, cls.__type__)

    require.user_id(id)
    main = aliased(Entity)
    q = db.session.query(main)
    q = q.filter(main.user_id == id)
    if 'category' in request.args:
        q = q.filter(main.category == request.args.get('category'))

    q2 = q
    match = aliased(Match)
    q = q.outerjoin(match, match.entity_id == main.id)

    for entity_id in request.args.getlist('entity'):
        other_match = aliased(Match)
        q = q.outerjoin(other_match, match.urn == other_match.urn)
        q = q.filter(other_match.entity_id == entity_id)

    q = q.group_by(main)
    count_field = count(func.distinct(match.urn))
    q = q.add_column(count_field)

    q2 = q2.group_by(main)
    count_field = count(func.distinct(None))
    q2 = q2.add_column(count_field)

    q = q.union(q2)
    q = q.order_by(main.text.asc())
    q = q.order_by(count_field.desc())

    q = q.distinct(main.text)

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
