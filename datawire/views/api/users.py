from flask import Blueprint
from flask.ext.login import current_user
from apikit import obj_or_404, request_data, Pager, jsonify

from datawire.model import User
from datawire.core import db
from datawire import authz


blueprint = Blueprint('users', __name__)


@blueprint.route('/api/1/users', methods=['GET'])
def index():
    authz.require(authz.logged_in())
    q = User.all()
    return jsonify(Pager(q))


@blueprint.route('/api/1/users/<login>', methods=['GET'])
def view(login):
    user = obj_or_404(User.by_login(login))
    data = user.to_dict()
    if user.id == current_user.id:
        data['email'] = user.email
    return jsonify(data)


@blueprint.route('/api/1/users/<login>', methods=['POST', 'PUT'])
def update(login):
    user = obj_or_404(User.by_login(login))
    authz.require(user.id == current_user.id)
    user.update(request_data())
    db.session.add(user)
    db.session.commit()
    return jsonify(user)
