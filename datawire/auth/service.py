from flask import request


def create():
    return request.user is not None


def view(service):
    return True


def _is_editor(service):
    if request.user is None:
        return False
    q = request.user.services.filter_by(id=service.id)
    return q.first() is not None


def admin(service):
    return _is_editor(service)


def publish(service):
    return _is_editor(service)


def delete(service):
    return _is_editor(service)
