from flask import url_for

from datawire.core import db
from datawire.model.util import ModelCore


class Event(db.Model, ModelCore):
    __tablename__ = 'event'

    key = db.Column(db.Unicode())
    label = db.Column(db.Unicode())
    description = db.Column(db.Unicode())
    template = db.Column(db.Unicode())
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'))

    frames = db.relationship('Frame', backref='event', lazy='dynamic',
                             cascade='all, delete-orphan', order_by='Frame.action_at.desc()')

    @classmethod
    def create(cls, data):
        # TODO: ensure this is the only event on this service with
        # this key.
        obj = cls()
        obj.key = data.get('key')
        obj.label = data.get('label')
        obj.description = data.get('description')
        obj.template = data.get('template')
        obj.service = data.get('service')
        db.session.add(obj)
        return obj

    def update(self, data):
        self.label = data.get('label')
        self.description = data.get('description')
        self.template = data.get('template')
        db.session.add(self)

    @classmethod
    def by_key(cls, service, key):
        q = db.session.query(cls)
        q = q.filter_by(service=service).filter_by(key=key)
        return q.first()

    def to_ref(self):
        return {
            'id': self.id,
            'key': self.key,
            'uri': url_for('events.get',
                service_key=self.service.key,
                event_key=self.key, _external=True),
            'template': self.template,
            'label': self.label
        }

    def to_dict(self):
        data = self.to_ref()
        data.update({
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })
        return data
