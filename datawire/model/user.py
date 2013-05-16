from datawire.core import db
from datawire.model.util import ModelCore, make_token


class User(db.Model, ModelCore):
    __tablename__ = 'user'

    screen_name = db.Column(db.Unicode())
    display_name = db.Column(db.Unicode())
    twitter_id = db.Column(db.Integer())
    facebook_id = db.Column(db.Integer())
    api_key = db.Column(db.Unicode(), default=make_token)
