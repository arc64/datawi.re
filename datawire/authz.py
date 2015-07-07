from flask import request
from flask.ext.login import current_user
from werkzeug.exceptions import Forbidden

from datawire.model import Collection


def authz_collections(action):
    if action == 'read' and request.authz_lists.get('read') is None:
        request.authz_lists['read'] = Collection.user_ids(current_user)
    if action == 'write' and request.authz_lists.get('write') is None:
        request.authz_lists['write'] = Collection.user_ids(current_user,
            include_public=False)  # noqa
    return request.authz_lists[action] or []


def collection_read(id):
    return id in authz_collections('read')


def collection_write(id):
    return id in authz_collections('write')


def logged_in():
    return current_user.is_authenticated()


def require(pred):
    if not pred:
        raise Forbidden("Sorry, you're not permitted to do this!")
