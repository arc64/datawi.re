from datawire.core import db
from datawire.model.util import ModelCore


class Service(db.Model, ModelCore):
    __tablename__ = 'service'

    key = db.Column(db.Unicode())
    label = db.Column(db.Unicode())

    frames = db.relationship('Frame', backref='service', lazy='dynamic', order_by='Frame.created_at.desc()')
    events = db.relationship('Event', backref='service', lazy='dynamic', order_by='Event.key.asc()')

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.screen_name,
            'label': self.display_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'events': self.events
        }
