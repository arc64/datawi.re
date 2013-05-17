from flask import request, render_template

from datawire.core import app
from datawire.exc import Unauthorized
from datawire.views.inbound import inbound

app.template_folder = '../templates'

app.register_blueprint(inbound, url_prefix='/api/1')

#@app.before_request
def basic_authentication():
    """ Attempt HTTP authentication via API keys on a per-request basis. """
    if 'Authorization' in request.headers:
        authorization = request.headers.get('Authorization')
        #authorization = authorization.split(' ', 1)[-1]
        #login, password = authorization.decode('base64').split(':', 1)
        try:
            pass
        #    magic
        #    logic.user.login({'login': login, 'password': password})
        except:
            raise Unauthorized('Invalid username or password.')


@app.route("/")
def index():
    return render_template('index.html')
