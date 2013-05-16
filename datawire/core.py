import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from datawire import default_settings

logging.basicConfig(level=logging.WARN)

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('DATAWIRE_SETTINGS', silent=True)

db = SQLAlchemy(app)
