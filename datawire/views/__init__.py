from flask import request, session, render_template

from datawire.core import app
from datawire.exc import Unauthorized
from datawire.model import User
from datawire.views.frames import frames
from datawire.views.sessions import sessions
from datawire.views.services import services
from datawire.views.events import events
from datawire.views.users import users
from datawire.views.entities import entities
from datawire.views.util import jsonify

app.register_blueprint(sessions, url_prefix='/api/1')
app.register_blueprint(frames, url_prefix='/api/1')
app.register_blueprint(services, url_prefix='/api/1')
app.register_blueprint(events, url_prefix='/api/1')
app.register_blueprint(users, url_prefix='/api/1')
app.register_blueprint(entities, url_prefix='/api/1')


@app.before_request
def authentication():
    """ Attempt HTTP authentication via API keys on a per-request basis. """
    auth_header = request.headers.get('Authorization')
    api_key = request.args.get('api_key')
    if auth_header is not None:
        auth_type, api_key = auth_header.split(' ', 1)
    if api_key is not None:
        try:
            request.user = User.by_api_key(api_key)
        except:
            raise Unauthorized('Invalid API key.')
    elif 'user_id' in session:
        request.user = User.by_id(session['user_id'])
    else:
        request.user = None


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def handle_exceptions(exc):
    """ Re-format exceptions to JSON. """
    body = {'status': exc.code,
            'name': exc.name,
            'description': exc.get_description(request.environ)}
    return jsonify(body, status=exc.code,
                   headers=exc.get_headers(request.environ))


@app.route("/")
@app.route("/profile")
def index():
    return render_template('index.html')
