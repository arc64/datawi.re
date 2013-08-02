#import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment
from pyes import ES

from datawire import default_settings

#logging.basicConfig(level=logging.WARN)

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('DATAWIRE_SETTINGS', silent=True)

db = SQLAlchemy(app)
assets = Environment(app)

elastic_index = app.config.get('ELASTICSEARCH_INDEX', 'datawire')
elastic = ES(app.config.get('ELASTICSEARCH_SERVER', '127.0.0.1:9200'),
             default_indices=elastic_index)
elastic.create_index_if_missing(elastic_index)

#js = Bundle('jquery.js', 'base.js', 'widgets.js',
#            filters='jsmin', output='gen/packed.js')
#assets.register('js_all', js)
