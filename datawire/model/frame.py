from datetime import datetime

from datawire.core import db


class Frame(db.Model):
    __tablename__ = 'frame'

    urn = db.Column(db.Unicode(), primary_key=True)
    hash = db.Column(db.Unicode())
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def to_urn(cls, frame):
        return 'urn:dwre:%(service)s:%(event)s:%(id)s' % frame

