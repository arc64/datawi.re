from flask import url_for
from datawire.core import db, app
from datawire.model.util import make_token


class Frame(db.Model):
    __tablename__ = 'frame'

    urn = db.Column(db.Unicode(), primary_key=True)
    hash = db.Column(db.Unicode(), index=True)
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    event_id = db.Column(db.Integer(), db.ForeignKey('event.id'))
    action_at = db.Column(db.DateTime, index=True)
    submitted_at = db.Column(db.DateTime, index=True)

    matches = db.relationship('Match', backref='frame', lazy='dynamic',
                              cascade='all, delete-orphan', order_by='Match.created_at.desc()')

    @classmethod
    def create(cls, service, event, data):
        obj = cls()
        obj.urn = data.get('urn')
        obj.hash = data.get('hash')
        obj.action_at = data.get('action_at')
        obj.submitted_at = data.get('submitted_at')
        obj.service = service
        obj.event = event
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

    def to_ref(self):
        from datawire.store import frame_url
        return {
            'urn': self.urn,
            'api_uri': url_for('frames.get', urn=self.urn, _external=True),
            'store_uri': frame_url(self.urn),
            'action_at': self.action_at,
            'submitted_at': self.submitted_at
        }

    @classmethod
    def all(cls):
        return db.session.query(cls)
