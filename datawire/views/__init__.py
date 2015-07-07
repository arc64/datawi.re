from colander import Invalid
from flask import request
from apikit import jsonify

from datawire.core import app, login_manager
from datawire.views.ui import ui # noqa
from datawire.model import User
from datawire.views.api.sessions import blueprint as sessions_api
from datawire.views.api.users import blueprint as users_api
from datawire.views.api.watchlists import blueprint as watchlists_api
from datawire.views.api.entities import blueprint as entities_api

app.register_blueprint(sessions_api)
app.register_blueprint(users_api)
app.register_blueprint(watchlists_api)
app.register_blueprint(entities_api)


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('X-API-Key') \
        or request.args.get('api_key')
    if api_key is not None:
        return User.by_api_key(api_key)


@app.before_request
def before():
    request.authz_lists = {}


@app.errorhandler(Invalid)
def handle_invalid(exc):
    exc.node.name = ''
    data = {
        'status': 400,
        'errors': exc.asdict()
    }
    return jsonify(data, status=400)
