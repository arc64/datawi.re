from flask import Blueprint, request, url_for

#from datawire.auth import require
from datawire.model import User
from datawire.views.util import jsonify, obj_or_404
from datawire.views.util import query_pager

users = Blueprint('users', __name__)


@users.route('/users')
def index():
    q = User.all()
    return query_pager(q, 'users.index')


@users.route('/users/<id>')
def get(id):
    user = obj_or_404(User.by_id(id))
    #require.service.view(service)
    return jsonify(user)
