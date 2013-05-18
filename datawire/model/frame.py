from datawire.core import db, app
from datawire.model.util import make_token


class Frame(db.Model):
    __tablename__ = 'frame'

    urn = db.Column(db.Unicode(), primary_key=True)
    hash = db.Column(db.Unicode(), index=True)
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    created_at = db.Column(db.DateTime)

    @classmethod
    def create(cls, service, data):
        obj = cls()
        obj.urn = data.get('urn')
        obj.hash = data.get('hash')
        obj.created_at = data.get('created_at')
        obj.service = service
        db.session.add(obj)
        return obj

    @classmethod
    def to_urn(cls, frame):
        uuid = make_token()
        instance = app.config.get('INSTANCE', 'dwre')
        return 'urn:%s:%s:%s:%s' % (instance, frame['service'],
                                    frame['event'], uuid)

    @classmethod
    def by_hash(cls, hash):
        q = db.session.query(cls).filter_by(hash=hash)
        return q.first()
