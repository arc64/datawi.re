from flask import request, session, render_template

from datawire.core import app
from datawire.exc import Unauthorized
from datawire.model import User
from datawire.views.frames import frames
from datawire.views.sessions import sessions
from datawire.views.util import jsonify

app.template_folder = '../templates'

app.register_blueprint(sessions)
app.register_blueprint(frames, url_prefix='/api/1')


@app.before_request
def authentication():
    """ Attempt HTTP authentication via API keys on a per-request basis. """
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        try:
            auth_type, api_key = auth_header.split(' ', 1)
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
def index():
    return render_template('index.html')
