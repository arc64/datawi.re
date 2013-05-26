from flask import Blueprint, request, url_for

from datawire.core import db
from datawire.auth import require
from datawire.model import User
from datawire.views.util import jsonify, obj_or_404
from datawire.views.pager import query_pager

users = Blueprint('users', __name__)


@users.route('/users')
def index():
    q = User.all()
    return query_pager(q, 'users.index')


@users.route('/users/<int:id>')
def get(id):
    user = obj_or_404(User.by_id(id))
    #require.service.view(service)
    return jsonify(user)


@users.route('/profile', methods=['GET'])
def profile_get():
    require.logged_in()
    data = request.user.to_dict()
    data['api_key'] = request.user.api_key
    data['email'] = request.user.email
    return jsonify(data)


@users.route('/profile', methods=['POST', 'PUT'])
def profile_save():
    print request.data
    require.logged_in()
    request.user.update(request.form)
    db.session.commit()
    return profile_get()
