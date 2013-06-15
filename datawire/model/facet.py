from flask import url_for
from formencode import FancyValidator, Invalid

from datawire.core import app

FACETS = app.config.get('FACETS')


class Facet(object):

    @classmethod
    def by_key(cls, key):
        for facet in cls.all():
            if facet['key'] == key:
                return facet

    @classmethod
    def all(cls):
        facets = []
        for facet in FACETS:
            facet['uri'] = url_for('entities.facet_get', key=facet['key'], _external=True)
            facets.append(facet)
        return facets


class ValidFacetName(FancyValidator):

    def _to_python(self, value, state):
        if Facet.by_key(value) is None:
            raise Invalid('Not a valid facet.', value, None)
        return value
