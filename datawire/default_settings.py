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
PROCESSING_WORKERS = 20

STORE_URL = 'file:///tmp/datawi.re/frames/'

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''

S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''

CATEGORIES = [
    {'key': 'persons', 'label': 'Persons', 'icon': 'icon-user'},
    {'key': 'orgs', 'label': 'Organisations', 'icon': 'icon-building'},
    {'key': 'topics', 'label': 'Topics', 'icon': 'icon-comment-alt'},
    {'key': 'places', 'label': 'Places', 'icon': 'icon-map-marker'},
]
