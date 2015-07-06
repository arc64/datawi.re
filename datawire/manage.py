from flask.ext.script import Manager
from flask.ext.assets import ManageAssets
from flask.ext.migrate import MigrateCommand
from flask.ext import migrate

from datawire.model import db
from datawire.views import app, assets

manager = Manager(app)
manager.add_command('assets', ManageAssets(assets))
manager.add_command('db', MigrateCommand)


@manager.command
def reset():
    """ Delete and re-create the search index and database. """
    db.drop_all()
    upgrade()


@manager.command
def upgrade():
    """ Create or upgrade the search index and database. """
    migrate.upgrade()


def main():
    manager.run()

if __name__ == "__main__":
    main()
