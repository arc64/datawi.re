from flask import url_for
import re
from formencode import Schema, validators

from datawire.core import db
from datawire.model.util import ModelCore
from datawire.model.category import ValidCategoryName


class EntitySchema(Schema):
    allow_extra_fields = True
    text = validators.String(min=3, max=512)
    category = ValidCategoryName()


class Entity(db.Model, ModelCore):
    __tablename__ = 'entity'

    text = db.Column(db.Unicode())
    category = db.Column(db.Unicode())

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    matches = db.relationship('Match', backref='entity', lazy='dynamic',
                              cascade='all, delete-orphan', order_by='Match.created_at.desc()')

    @classmethod
    def create(cls, data, user):
        obj = cls()
        data = EntitySchema().to_python(data)
        obj.user = user
        obj.text = data.get('text')
        obj.category = data.get('category')
        db.session.add(obj)
        return obj

    def update(self, data):
        data = EntitySchema().to_python(data)
        self.text = data.get('text')
        self.category = data.get('category')
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @property
    def pattern(self):
        return re.compile(self.text, re.I | re.M)

    @classmethod
    def by_user_and_id(cls, user, id):
        q = db.session.query(cls).filter_by(user=user)
        q = q.filter_by(id=id)
        return q.first()

    @classmethod
    def by_text(cls, text):
        q = db.session.query(cls).filter_by(text=text)
        return q.first()

    @classmethod
    def by_category(cls, category):
        q = db.session.query(cls).filter_by(category=category)
        return q.first()

    def to_ref(self):
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
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
