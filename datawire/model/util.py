import uuid
from datetime import datetime
from hashlib import sha1

from datawire.core import db


class ModelCore(object):
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    @classmethod
    def by_id(cls, id):
        q = db.session.query(cls).filter_by(id=id)
        return q.first()

    @classmethod
    def all(cls):
        return db.session.query(cls)


def make_token():
    return uuid.uuid4().get_hex()[15:]


def data_hash(data):
    # TODO: This has plenty of collisions, maybe get it right some time.
    if isinstance(data, (list, tuple)):
        return '||'.join(map(data_hash, data))
    if isinstance(data, datetime):
        return data.isoformat()
    if isinstance(data, dict):
        d = [(k, data_hash(v)) for k, v in sorted(data.items())]
        return sha1(data_hash(d)).hexdigest()
    return unicode(data)
