from datawire.core import db
from datawire.model.util import ModelCore


class Event(db.Model, ModelCore):
    __tablename__ = 'event'

    key = db.Column(db.Unicode())
    label = db.Column(db.Unicode())
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))
