from flask import url_for

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
