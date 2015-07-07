from flask import session, Blueprint, redirect, request
from flask.ext.login import login_user, logout_user, current_user
from apikit import jsonify

from datawire import authz
from datawire.core import db, app, oauth, url_for
from datawire.model import User


blueprint = Blueprint('sessions', __name__)


twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1.1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key=app.config.get('TWITTER_API_KEY'),
                           consumer_secret=app.config.get('TWITTER_API_SECRET'))


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@blueprint.route('/api/1/sessions')
def status():
    return jsonify({
        'logged_in': authz.logged_in(),
        'api_key': current_user.api_key if authz.logged_in() else None,
        'user': current_user if authz.logged_in() else None,
        'logout': url_for('.logout')
    })


@blueprint.route('/api/1/sessions/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(request.args.get('next_url', url_for('ui')))


@blueprint.route('/api/1/sessions/login')
def login():
    if current_user.is_authenticated():
        return redirect(url_for('ui'))
    session.clear()
    callback = url_for('.authorized')
    session['next_url'] = request.args.get('next_url', url_for('ui'))
    return twitter.authorize(callback=callback)


@blueprint.route('/api/1/sessions/callback')
@twitter.authorized_handler
def authorized(resp):
    next_url = session.get('next_url', url_for('ui'))
    if resp is None or 'oauth_token' not in resp:
        return redirect(next_url)
    session['twitter_token'] = (resp['oauth_token'],
                                resp['oauth_token_secret'])
    res = twitter.get('users/show.json?user_id=%s' % resp.get('user_id'))
    data = {
        'login': res.data.get('screen_name'),
        'oauth_id': res.data.get('id')
    }
    user = User.load(data)
    db.session.commit()
    login_user(user, remember=True)
    return redirect(next_url)
