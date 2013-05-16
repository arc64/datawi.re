from datawire.core import db
from datawire.model.util import ModelCore, make_token


class User(db.Model, ModelCore):
    __tablename__ = 'user'

    screen_name = db.Column(db.Unicode())
    display_name = db.Column(db.Unicode())
    twitter_id = db.Column(db.Integer())
    facebook_id = db.Column(db.Integer())
    api_key = db.Column(db.Unicode(), default=make_token)

    @classmethod
    def create(cls, data):
        obj = cls()
        obj.screen_name = data.get('screen_name')
        obj.display_name = data.get('display_name')
        obj.twitter_id = data.get('twitter_id')
        obj.facebook_id = data.get('facebook_id')
        db.session.add(obj)
        return obj

    @classmethod
    def by_screen_name(cls, screen_name):
        q = db.session.query(cls)
        q = q.filter_by(screen_name=screen_name)
        return q.first()

    def to_dict(self):
        return {
            'id': self.id,
            'screen_name': self.screen_name,
            'display_name': self.display_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
