from flask import url_for
from formencode import FancyValidator, Invalid

from datawire.core import app

CATEGORIES = app.config.get('CATEGORIES')


class Category(object):

    @classmethod
    def by_key(cls, key):
        for category in cls.all():
            if category['key'] == key:
                return category

    @classmethod
    def all(cls):
        categories = []
        for category in CATEGORIES:
            category['uri'] = url_for('entities.category_get',
                                      key=category['key'],
                                      _external=True)
            categories.append(category)
        return categories


class ValidCategoryName(FancyValidator):

    def _to_python(self, value, state):
        if Category.by_key(value) is None:
            raise Invalid('Not a valid category.', value, None)
        return value
