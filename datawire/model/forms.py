import colander
from colander import Invalid # noqa

PERSON = 'Person'
COMPANY = 'Company'
ORGANIZATION = 'Organization'
OTHER = 'Other'
CATEGORIES = [PERSON, COMPANY, ORGANIZATION, OTHER]


class Ref(object):

    def deserialize(self, node, cstruct):
        if cstruct is colander.null:
            return colander.null
        value = self.decode(cstruct)
        if value is None:
            raise colander.Invalid(node, 'Missing')
        return value

    def cstruct_children(self, node, cstruct):
        return []


class UserRef(Ref):

    def decode(self, cstruct):
        from aleph.model.user import User

        if isinstance(cstruct, User):
            return cstruct
        if isinstance(cstruct, (basestring, int)):
            return User.by_id(cstruct)
        if isinstance(cstruct, dict):
            return self.decode(cstruct.get('id'))
        return None


class ListRef(Ref):

    def decode(self, cstruct):
        from aleph.model.watchlist import Watchlist

        if isinstance(cstruct, Watchlist):
            return cstruct
        if isinstance(cstruct, (basestring, int)):
            return Watchlist.by_id(cstruct)
        if isinstance(cstruct, dict):
            return self.decode(cstruct.get('id'))
        return None


class UserForm(colander.MappingSchema):
    email = colander.SchemaNode(colander.String(),
                                validator=colander.Email())
    login = colander.SchemaNode(colander.String())


class WatchlistForm(colander.MappingSchema):
    slug = colander.SchemaNode(colander.String())
    public = colander.SchemaNode(colander.Boolean())


class EntitySelectors(colander.SequenceSchema):
    selector = colander.SchemaNode(colander.String())


class EntityForm(colander.MappingSchema):
    label = colander.SchemaNode(colander.String())
    category = colander.SchemaNode(colander.String(),
                                   validator=colander.OneOf(CATEGORIES))
    selectors = EntitySelectors()
    watchlist = colander.SchemaNode(ListRef())
