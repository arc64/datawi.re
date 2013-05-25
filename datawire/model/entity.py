from flask import url_for
from formencode import Schema, FancyValidator, Invalid, validators

from datawire.core import db, app
from datawire.model.util import ModelCore

FACETS = app.config.get('FACETS')


class ValidFacetName(FancyValidator):

    def _to_python(self, value, state):
        if Facet.by_key(value) is None:
            raise Invalid('Not a valid facet.', value, None)
        return value


class EntitySchema(Schema):
    allow_extra_fields = True
    text = validators.String(min=3, max=512)
    facet = ValidFacetName()


class Facet(object):

    @classmethod
    def by_key(cls, key):
        for facet in cls.all():
            if facet['key'] == key:
                return facet

    @classmethod
    def all(cls):
        facets = []
        for facet in FACETS:
            facet['uri'] = url_for('entities.facet_get', key=facet['key'], _external=True)
            facets.append(facet)
        return facets


class Entity(db.Model, ModelCore):
    __tablename__ = 'entity'

    text = db.Column(db.Unicode())
    facet = db.Column(db.Unicode())

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    @classmethod
    def create(cls, data, user):
        obj = cls()
        data = EntitySchema().to_python(data)
        obj.user = user
        obj.text = data.get('text')
        obj.facet = data.get('facet')
        db.session.add(obj)
        return obj

    def update(self, data):
        data = EntitySchema().to_python(data)
        self.text = data.get('text')
        self.facet = data.get('facet')
        db.session.add(self)

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
