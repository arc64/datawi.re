from flask import url_for

from datawire.core import db
from datawire.model.util import ModelCore

editors = db.Table('editor',
                   db.Column('service_id', db.Integer(), db.ForeignKey('service.id')),
                   db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
)


class Service(db.Model, ModelCore):
    __tablename__ = 'service'

    key = db.Column(db.Unicode())
    label = db.Column(db.Unicode())
    description = db.Column(db.Unicode())
    url = db.Column(db.Unicode())

    frames = db.relationship('Frame', backref='service', lazy='dynamic',
                             cascade='all, delete-orphan', order_by='Frame.created_at.desc()')
    events = db.relationship('Event', backref='service', lazy='dynamic',
                             cascade='all, delete-orphan', order_by='Event.key.asc()')
    editors = db.relationship('User', secondary=editors,
                              backref=db.backref('services', lazy='dynamic'))

    @classmethod
    def create(cls, data):
        # TODO: ensure this is the only service with this key.
        obj = cls()
        obj.key = data.get('key')
        obj.label = data.get('label')
        obj.description = data.get('description')
        obj.url = data.get('url')
        db.session.add(obj)
        return obj

    def update(self, data):
        self.label = data.get('label')
        self.description = data.get('description')
        self.url = data.get('url')
        db.session.add(self)

    @classmethod
    def by_key(cls, key):
        q = db.session.query(cls).filter_by(key=key)
        return q.first()

    def to_ref(self):
        return {
            'id': self.id,
            'key': self.key,
            'uri': url_for('services.get', key=self.key, _external=True),
            'label': self.label
        }

    def to_dict(self):
        data = self.to_ref()
        data.update({
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'description': self.description,
            'url': self.url,
            'events': [e.to_ref() for e in self.events],
            'editors': self.editors
        })
        return data
