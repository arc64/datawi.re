from flask import Blueprint, request
from flask.ext.login import current_user
from werkzeug.exceptions import BadRequest
from apikit import obj_or_404, jsonify, Pager, request_data

from datawire.model import Entity, Collection, db
from datawire.model.forms import EntityForm
from datawire import authz

blueprint = Blueprint('entities', __name__)


@blueprint.route('/api/1/entities', methods=['GET'])
def index():
    collection_ids = Collection.user_ids(current_user)
    filter_collections = request.args.getlist('collection')
    if len(filter_collections):
        try:
            collection_ids = [l for l in collection_ids if l
                              in filter_collections]
        except ValueError:
            raise BadRequest()

    prefix = request.args.get('prefix')
    q = Entity.by_collection(collection_ids, prefix=prefix)
    return jsonify(Pager(q))


@blueprint.route('/api/1/entities', methods=['POST', 'PUT'])
def create():
    data = EntityForm().deserialize(request_data())
    authz.require(data['collection'])
    authz.require(authz.collection_write(data['collection'].id))
    entity = Entity.create(data, current_user)
    db.session.commit()
    return view(entity.id)


@blueprint.route('/api/1/entities/_suggest', methods=['GET'])
def suggest():
    prefix = request.args.get('prefix')
    results = Entity.suggest_prefix(prefix, authz.authz_collection('read'))
    return jsonify({'results': results})


@blueprint.route('/api/1/entities/<id>', methods=['GET'])
def view(id):
    entity = obj_or_404(Entity.by_id(id))
    authz.require(authz.collection_read(entity.collection_id))
    return jsonify(entity)


@blueprint.route('/api/1/entities/<id>', methods=['POST', 'PUT'])
def update(id):
    entity = obj_or_404(Entity.by_id(id))
    authz.require(authz.collection_write(entity.collection_id))
    data = EntityForm().deserialize(request_data())
    authz.require(data['list'])
    authz.require(authz.collection_write(data['list'].id))
    entity.update(data)
    db.session.commit()
    return view(entity.id)


@blueprint.route('/api/1/entities/<id>', methods=['DELETE'])
def delete(id):
    entity = obj_or_404(Entity.by_id(id))
    authz.require(authz.collection_write(entity.collection_id))
    entity.delete()
    db.session.commit()
    return jsonify({'status': 'ok'})
