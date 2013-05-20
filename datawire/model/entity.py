from flask import url_for

from datawire.core import db
from datawire.model.util import ModelCore


class Entity(db.Model, ModelCore):
    __tablename__ = 'entity'

    text = db.Column(db.Unicode())
    facet = db.Column(db.Unicode())

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    @classmethod
    def create(cls, user, data):
        obj = cls()
        obj.user = user
        obj.text = data.get('text')
        obj.facet = data.get('facet')
        db.session.add(obj)
        return obj

    @classmethod
    def by_text(cls, text):
        q = db.session.query(cls).filter_by(text=text)
        return q.first()

    @classmethod
    def by_facet(cls, facet):
        q = db.session.query(cls).filter_by(facet=facet)
        return q.first()

    def to_ref(self):
        return {
            'id': self.id,
            'text': self.text,
            'facet': self.facet,
            'user_id': self.user_id
        }

    def to_dict(self):
        data = self.to_ref()
        data.update({
            'user': self.user.to_ref(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        })
        return data
