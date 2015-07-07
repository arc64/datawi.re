import logging
from datetime import datetime

from sqlalchemy import or_

from datawire.core import db, url_for
from datawire.model.user import User
from datawire.model.forms import CollectionForm

log = logging.getLogger(__name__)


class Collection(db.Model):
    id = db.Column(db.Unicode(50), primary_key=True)
    slug = db.Column(db.Unicode(250))
    public = db.Column(db.Boolean, default=False)

    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'),
                         nullable=True)
    owner = db.relationship(User)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'api_url': url_for('collections.view', id=self.id),
            'entities_api_url': url_for('entities.index', list=self.id),
            'slug': self.slug,
            'public': self.public,
            'owner': self.owner,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def create(cls, data, user):
        lst = cls()
        lst.update(data, user)
        lst.owner = user
        db.session.add(lst)
        return lst

    def update(self, data, user):
        data = CollectionForm().deserialize(data)
        self.slug = data.get('slug')
        if data.get('public') is not None:
            self.public = data.get('public')

    def delete(self):
        # for entity in self.entities:
        #     entity.delete()
        db.session.delete(self)

    @classmethod
    def by_slug(cls, login, slug):
        q = db.session.query(cls).filter_by(slug=slug)
        q = q.filter(cls.owner.login == login)
        return q.first()

    @classmethod
    def by_id(cls, id):
        q = db.session.query(cls).filter_by(id=id)
        return q.first()

    @classmethod
    def user_ids(cls, user, include_public=True):
        logged_in = user is not None and user.is_authenticated()
        q = db.session.query(cls.id)
        conds = []
        if include_public:
            conds.append(cls.public == True) # noqa
        if logged_in:
            conds.append(cls.owner_id == user.id)
        if not len(conds):
            return []
        if not (logged_in and user.is_admin):
            q = q.filter(or_(*conds))
        return [c.id for c in q.all()]

    @classmethod
    def all_by_user(cls, user):
        q = db.session.query(cls)
        q = q.filter(cls.id.in_(cls.user_ids(user)))
        q = q.order_by(cls.id.desc())
        return q

    @property
    def terms(self):
        from aleph.model.entity import Entity
        from aleph.model.selector import Selector
        q = db.session.query(Selector.normalized)
        q = q.join(Entity, Entity.id == Selector.entity_id)
        q = q.filter(Entity.watchlist_id == self.id)
        q = q.distinct()
        return set([r[0] for r in q])

    def __repr__(self):
        return '<Watchlist(%r, %r)>' % (self.id, self.slug)

    def __unicode__(self):
        return self.slug
