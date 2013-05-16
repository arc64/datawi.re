from datawire.core import db
from datawire.model.util import ModelCore


class Event(db.Model, ModelCore):
    __tablename__ = 'event'

    key = db.Column(db.Unicode())
    label = db.Column(db.Unicode())
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.screen_name,
            'label': self.display_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
