from flask import url_for

from datawire.core import db
from datawire.model.util import ModelCore


class Match(db.Model, ModelCore):
    __tablename__ = 'match'

    urn = db.Column(db.Unicode(), db.ForeignKey('frame.urn'))
    field = db.Column(db.Unicode())
    entity_id = db.Column(db.Integer(), db.ForeignKey('entity.id'))

    @classmethod
    def create(cls, urn, field, entity):
        obj = cls()
        obj.urn = urn
        obj.field = field
        obj.entity = entity
        db.session.add(obj)
        return obj

    @classmethod
    def exists(cls, urn, entity):
        q = db.session.query(cls)
        q = q.filter_by(urn=urn)
        q = q.filter_by(entity=entity)
        return q.first()

    def to_ref(self):
        data = self.frame.to_ref()
        data.update({
            'id': self.id,
            'field': self.field,
            'matched_at': self.created_at,
            'entity_id': self.entity_id
        })
        return data

    def to_dict(self):
        data = self.to_ref()
        data.update({
            'entity': self.entity
        })
        return data
