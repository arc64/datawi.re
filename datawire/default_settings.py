from os import environ as env, path

DEBUG = True
ASSETS_DEBUG = DEBUG

APP_TITLE = 'datawire.local'
APP_NAME = 'datwire'

SECRET_KEY = env.get('SECRET_KEY', 'banana umbrella')

SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL', 'sqlite:////Users/fl/Code/datawi.re/db.sqlite3')

ALEMBIC_DIR = path.join(path.dirname(__file__), 'migrate')
ALEMBIC_DIR = path.abspath(ALEMBIC_DIR)

TWITTER_API_KEY = None
TWITTER_API_SECRET = None

CELERY_ALWAYS_EAGER = False
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_BROKER_URL = env.get('RABBITMQ_BIGWIG_URL',
                            'amqp://guest:guest@localhost:5672//')
CELERY_IMPORTS = ('datawire.queue')
