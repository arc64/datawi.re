from datawire.core import db
from datawire.model.util import ModelCore


class Service(db.Model, ModelCore):
    __tablename__ = 'service'

    key = db.Column(db.Unicode())
    label = db.Column(db.Unicode())

    frames = db.relationship('Frame', backref='service', lazy='dynamic', order_by='Frame.created_at.desc()')
