import logging
from datetime import datetime

from datawire.core import db, login_manager, url_for
from datawire.model.util import make_token
from datawire.model.forms import UserForm

log = logging.getLogger(__name__)


@login_manager.user_loader
def load_user(login):
    return User.by_login(login)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Unicode(255))
    email = db.Column(db.Unicode, nullable=True)
    oauth_id = db.Column(db.Unicode)
    api_key = db.Column(db.Unicode, default=make_token)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.login

    def __repr__(self):
        return '<User(%r,%r)>' % (self.id, self.login)

    def __unicode__(self):
        return self.login

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'api_url': url_for('users.view', login=self.login)
        }

    def update(self, data):
        data = UserForm().deserialize(data)
        self.email = data.get('email')

    @classmethod
    def load(cls, data):
        user = cls.by_oauth_id(data.get('oauth_id'))

        if user is None:
            user = cls()
            user.login = data.get('login')
            user.oauth_id = data.get('oauth_id')

        if data.get('email'):
            # FIXME: better to overwrite with upstream or keep?
            user.email = data.get('email')
        db.session.add(user)
        return user

    @classmethod
    def all(cls):
        q = db.session.query(cls).filter_by(active=True)
        return q

    @classmethod
    def by_login(cls, login):
        q = db.session.query(cls).filter_by(login=login)
        return q.first()

    @classmethod
    def by_api_key(cls, api_key):
        q = db.session.query(cls).filter_by(api_key=api_key)
        return q.first()

    @classmethod
    def by_oauth_id(cls, oauth_id):
        q = db.session.query(cls).filter_by(oauth_id=unicode(oauth_id))
        return q.first()
