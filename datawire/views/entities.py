from flask import Blueprint, request, url_for
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import or_, and_, func
from sqlalchemy.orm import aliased

from datawire.core import db, elastic, elastic_index
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

    q = Entity.all().filter(Entity.user_id == id)
    if 'category' in request.args:
        q = q.filter(Entity.category == request.args.get('category'))
    all_entities = [{"term": {"entities": e.id}} for e in q]

    esq = {
        "query": {
            "filtered": {
                "query": {"match_all": {}}, "filter": {}
            }
        },
        "size": 0,
        "facets": {
            "entities": {
                "terms": {"field": "entities"}
            },
            "global": {
                "terms": {"field": "entities"},
                "global": True,
                "facet_filter": {"or": all_entities}
            }
        }
    }

    filters = request.args.getlist('entity')
    if len(filters):
        esq['query']['filtered']['filter']['and'] = []
        for entity_id in filters:
            fq = {"term": {"entities": entity_id}}
            esq['query']['filtered']['filter']['and'].append(fq)
    else:
        esq['query']['filtered']['filter']['or'] = all_entities

    res = elastic.search_raw(esq, elastic_index, 'frame')
    filtered_counts = res['facets']['entities']['terms']
    filtered_counts = dict([(int(c['term']), c['count']) for c in filtered_counts])
    total_counts = res['facets']['global']['terms']
    total_counts = dict([(int(c['term']), c['count']) for c in total_counts])

    q = Entity.all().filter(Entity.user_id == id)
    if 'category' in request.args:
        q = q.filter(Entity.category == request.args.get('category'))

    def transform_result(entity):
        data = entity.to_ref()
        data['filtered_count'] = filtered_counts.get(entity.id, 0)
        data['total_count'] = total_counts.get(entity.id, 0)
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
