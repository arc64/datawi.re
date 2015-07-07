from flask import request
from flask.ext.login import current_user
from werkzeug.exceptions import Forbidden

from datawire.model import Watchlist


def authz_watchlists(action):
    if action == 'read' and request.authz_lists.get('read') is None:
        request.authz_lists['read'] = Watchlist.user_list_ids(current_user)
    if action == 'write' and request.authz_lists.get('write') is None:
        request.authz_lists['write'] = Watchlist.user_list_ids(current_user,
            include_public=False) # noqa
    return request.authz_lists[action] or []


def list_read(id):
    return id in authz_watchlists('read')


def list_write(id):
    return id in authz_watchlists('write')


def logged_in():
    return current_user.is_authenticated()


def require(pred):
    if not pred:
        raise Forbidden("Sorry, you're not permitted to do this!")
