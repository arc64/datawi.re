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
def install(filename):
    """ Load or update a service configuration form a JSON configuration. """
    with open(filename, 'rb') as fh:
        data = json.load(fh)
        service = Service.by_key(data.get('key'))
        if service is None:
            service = Service.create(data)
        else:
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
        service.editors = []
        for editor_id in data.get('editors', [1]):
            user = User.by_id(editor_id)
            service.editors.append(user)
        db.session.commit()


@manager.command
def delete(key):
    """ Delete a service configuration from the database. """
    service = Service.by_key(key)
    if service is None:
        raise ValueError("Service doesn't exist: %s" % key)
    db.session.delete(service)
    db.session.commit()


@manager.command
def match(urn):
    """ Test entity matching. """
    from datawire.store import load_frame
    from datawire.processing.matching import match
    frame = load_frame(urn)
    match(frame)


@manager.command
def matchall():
    """ Re-do all matching. """
    from datawire.store import load_frame
    from datawire.model import Frame
    from datawire.processing.matching import match
    for frame_ref in Frame.all():
        frame = load_frame(frame_ref.urn)
        if frame is None:
            continue
        match(frame)


@manager.command
def process():
    """ Process background tasks from the queue. """
    from datawire.processing import process
    process()


if __name__ == "__main__":
    manager.run()
