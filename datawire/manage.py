from flask.ext.script import Manager

from datawire.core import app, db
from datawire.model import Service

manager = Manager(app)


@manager.command
def create_db():
    """ Create the database entities. """
    db.create_all()


if __name__ == "__main__":
    manager.run()
