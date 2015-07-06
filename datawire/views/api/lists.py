from flask import Blueprint  # , request
from flask.ext.login import current_user
from apikit import obj_or_404, jsonify, Pager, request_data

from datawire.model import List, db
from datawire import authz

blueprint = Blueprint('lists', __name__)


@blueprint.route('/api/1/lists', methods=['GET'])
def index():
    q = List.all_by_user(current_user)
    data = Pager(q).to_dict()
    results = []
    for lst in data.pop('results'):
        ldata = lst.to_dict()
        ldata['can_write'] = authz.list_write(lst.id)
        results.append(ldata)
    data['results'] = results
    return jsonify(data)


@blueprint.route('/api/1/lists', methods=['POST', 'PUT'])
def create():
    authz.require(authz.logged_in())
    data = request_data()
    data['creator'] = current_user
    if 'users' not in data:
        data['users'] = []
    lst = List.create(data, current_user)
    db.session.commit()
    return view(lst.id)


@blueprint.route('/api/1/lists/<int:id>', methods=['GET'])
def view(id):
    authz.require(authz.list_read(id))
    lst = obj_or_404(List.by_id(id))
    data = lst.to_dict()
    data['can_write'] = authz.list_write(id)
    if data['can_write']:
        data['users'] = [u.id for u in lst.users]
    return jsonify(data)


@blueprint.route('/api/1/lists/<int:id>', methods=['POST', 'PUT'])
def update(id):
    authz.require(authz.list_write(id))
    lst = obj_or_404(List.by_id(id))
    lst.update(request_data(), current_user)
    db.session.add(lst)
    db.session.commit()
    return view(id)


@blueprint.route('/api/1/lists/<int:id>', methods=['DELETE'])
def delete(id):
    authz.require(authz.list_write(id))
    lst = obj_or_404(List.by_id(id))
    lst.delete()
    db.session.commit()
    return jsonify({'status': 'ok'})
