import os

DEBUG = True
ASSETS_DEBUG = True
SECRET_KEY = os.environ.get('DATAWIRE_SECRET')

INSTANCE = 'dwre'

SMTP_SENDER = 'info@datawi.re'
SMTP_SERVER = 'datawi.re'
SYSADMINS = ['friedrich@pudo.org']

SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
AMQP_QUEUE_URI = 'amqp://guest:guest@localhost//'

STORE_URL = 'file:///tmp/datawi.re/frames/'

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''

S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''

FACETS = [
    {'key': 'persons', 'label': 'Persons'},
    {'key': 'orgs', 'label': 'Organisations'},
    {'key': 'topics', 'label': 'Topics'},
    {'key': 'places', 'label': 'Places'},
]
