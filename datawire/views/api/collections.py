from flask import Blueprint  # , request
from flask.ext.login import current_user
from apikit import obj_or_404, jsonify, Pager, request_data

from datawire.model import Collection, db
from datawire import authz

blueprint = Blueprint('collections', __name__)


@blueprint.route('/api/1/collections', methods=['GET'])
def index():
    q = Collection.all_by_user(current_user)
    data = Pager(q).to_dict()
    results = []
    for lst in data.pop('results'):
        ldata = lst.to_dict()
        ldata['permissions'] = {
            'write': authz.collection_write(lst.id)
        }
        results.append(ldata)
    data['results'] = results
    return jsonify(data)


@blueprint.route('/api/1/collections', methods=['POST', 'PUT'])
def create():
    authz.require(authz.logged_in())
    data = request_data()
    data['creator'] = current_user
    lst = Collection.create(data, current_user)
    db.session.commit()
    return view(lst.id)


@blueprint.route('/api/1/collections/<id>', methods=['GET'])
def view(id):
    authz.require(authz.collection_read(id))
    coll = obj_or_404(Collection.by_id(id))
    data = coll.to_dict()
    data['can_write'] = authz.collection_write(id)
    return jsonify(data)


@blueprint.route('/api/1/collections/<id>', methods=['POST', 'PUT'])
def update(id):
    authz.require(authz.collection_write(id))
    coll = obj_or_404(Collection.by_id(id))
    coll.update(request_data(), current_user)
    db.session.add(coll)
    db.session.commit()
    return view(id)


@blueprint.route('/api/1/collections/<id>', methods=['DELETE'])
def delete(id):
    authz.require(authz.collection_write(id))
    coll = obj_or_404(Collection.by_id(id))
    coll.delete()
    db.session.commit()
    return jsonify({'status': 'ok'})
