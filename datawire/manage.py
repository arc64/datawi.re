from flask.ext.script import Manager

from datawire.core import app, db
from datawire.model import User
from datawire.views import index

manager = Manager(app)


@manager.command
def createdb():
    """ Create the database entities. """
    db.create_all()
    admin_data = {'screen_name': 'admin', 'display_name': 'Systems Admin'}
    if User.by_screen_name(admin_data.get('screen_name')) is None:
        admin = User.create(admin_data)
    db.session.commit() 


if __name__ == "__main__":
    manager.run()
