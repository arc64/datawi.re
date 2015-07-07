import logging
from flask import Flask
from flask import url_for as _url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.oauth import OAuth
# from kombu import Exchange, Queue
# from celery import Celery

from datawire import default_settings

logging.basicConfig(level=logging.DEBUG)

# specific loggers
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('amqp').setLevel(logging.INFO)

app = Flask(__name__, static_folder='../frontend')
app.config.from_object(default_settings)
app.config.from_envvar('DATAWIRE_SETTINGS', silent=True)
app_name = app.config.get('APP_NAME')

db = SQLAlchemy(app)
migrate = Migrate(app, db, directory=app.config.get('ALEMBIC_DIR'))

oauth = OAuth()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'ui'

# queue_name = app_name + '_q'
# app.config['CELERY_DEFAULT_QUEUE'] = queue_name
# app.config['CELERY_QUEUES'] = (
#     Queue(queue_name, Exchange(queue_name), routing_key=queue_name),
# )

# celery = Celery(app_name, broker=app.config['CELERY_BROKER_URL'])
# celery.config_from_object(app.config)


def url_for(*a, **kw):
    try:
        kw['_external'] = True
        return _url_for(*a, **kw)
    except RuntimeError:
        return None
