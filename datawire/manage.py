import json
from flask.ext.script import Manager

from datawire.core import app, db
from datawire.model import User, Service, Event
from datawire.views import index

manager = Manager(app)


@manager.command
def createdb():
    """ Create the database entities. """
    db.create_all()
    admin_data = {'screen_name': 'admin', 'name': 'Systems Admin'}
    if User.by_screen_name(admin_data.get('screen_name')) is None:
        User.create(admin_data)
    db.session.commit()


@manager.command
def createservice(filename):
    """ Load a service configuration form a JSON configuration. """
    with open(filename, 'rb') as fh:
        data = json.load(fh)
        events = data.pop('events', [])
        service = Service.by_key(data.get('key'))
        if service is not None:
            raise ValueError("Service already exists: %s" % data.get('key'))
        service = Service.create(data)
        for event_data in events:
            event_data['service'] = service
            Event.create(event_data)
        db.session.commit()


@manager.command
def deleteservice(key):
    """ Delete a service configuration from the database. """
    service = Service.by_key(key)
    if service is None:
        raise ValueError("Service doesn't exist: %s" % key)
    db.session.delete(service)
    db.session.commit()


if __name__ == "__main__":
    manager.run()
