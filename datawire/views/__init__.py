from flask import request, render_template

from datawire.core import app
from datawire.exc import Unauthorized
#from datawire.model import User
from datawire.views.inbound import inbound
from datawire.views.util import jsonify

app.template_folder = '../templates'

app.register_blueprint(inbound, url_prefix='/api/1')


@app.before_request
def basic_authentication():
    """ Attempt HTTP authentication via API keys on a per-request basis. """
    auth_header = request.headers.get('Authorization')
    if auth_header is not None:
        try:
            auth_type, api_key = auth_header.split(' ', 1)
            
        except:
            raise Unauthorized('Invalid username or password.')


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
