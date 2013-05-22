import json
from flask.ext.script import Manager
from flask.ext.assets import ManageAssets

from datawire.core import app, db, assets
from datawire.model import User, Service, Event
from datawire.views import index
from datawire.logs import logger

manager = Manager(app)
manager.add_command("assets", ManageAssets(assets))


@manager.command
def createdb():
    """ Create the database entities. """
    db.create_all()
    admin_data = {'screen_name': 'admin', 'name': 'Systems Admin'}
    if User.by_screen_name(admin_data.get('screen_name')) is None:
        user = User.create(admin_data)
        db.session.flush()
        user.api_key = app.config.get('SECRET_KEY')
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
        user = User.by_screen_name('admin')
        service.editors.append(user)
        db.session.commit()


@manager.command
def updateservice(filename):
    """ Update a service configuration form a JSON configuration. """
    with open(filename, 'rb') as fh:
        data = json.load(fh)
        service = Service.by_key(data.get('key'))
        if service is None:
            raise ValueError("Service doesn't exist: %s" % data.get('key'))
        service.update(data)
        events = []
        for event_data in data.get('events', []):
            event_data['service'] = service
            event = Event.by_key(service, event_data['key'])
            if event is None:
                event = Event.create(event_data)
            else:
                event.update(event_data)
            events.append(event)
        service.events = events
        db.session.commit()


@manager.command
def deleteservice(key):
    """ Delete a service configuration from the database. """
    service = Service.by_key(key)
    if service is None:
        raise ValueError("Service doesn't exist: %s" % key)
    db.session.delete(service)
    db.session.commit()


@manager.command
def process():
    """ Process background tasks from the queue. """
    from datawire.processing import process
    process()


if __name__ == "__main__":
    manager.run()
