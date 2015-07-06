from rdflib import Literal, URIRef, Namespace, Graph
from rdflib import ConjunctiveGraph
from rdflib.plugins.memory import IOMemory
from rdflib.namespace import DC, FOAF, OWL, SKOS, RDFS, DCTERMS

OPENGOV = Namespace('http://www.w3.org/ns/opengov#')
VCARD = Namespace('http://www.w3.org/2006/vcard/ns#')
ORG = Namespace('http://www.w3.org/ns/org#')
PERSON = Namespace('http://www.w3.org/ns/person#')
BIO = Namespace('http://purl.org/vocab/bio/0.1/')
SCHEMA = Namespace('http://schema.org/')
DW = Namespace('http://datawi.re/ns/0.1/')

NAMESPACES = {
    'owl': OWL,
    'dc': DC,
    'dcterms': DCTERMS,
    'rdfs': RDFS,
    'foaf': FOAF,
    'skos': SKOS,
    'opengov': OPENGOV,
    'vcard': VCARD,
    'org': ORG,
    'person': PERSON,
    'schema': SCHEMA,
    'dw': DW
}


class Property(object):

    def __init__(self, pred):
        self.pred = pred


class Person(object):
    type = PERSON.Person
    name = FOAF.name
    email = SCHEMA.email
    gender = FOAF.gender
    birth_date = SCHEMA.birthDate
    death_date = SCHEMA.deathDate
    summary = BIO.olb
    biography = BIO.biography
    identifier = FOAF.nick
    other_names = DCTERMS.alternative
    links = RDFS.seeAlso


class Organization(object):
    type = ORG.Organization
    name = SKOS.prefLabel
    other_names = SKOS.altLabel
    identifiers = ORG.identifier
    founding_date = SCHEMA.foundingDate
    dissolution_date = SCHEMA.dissolutionDate
    links = RDFS.seeAlso


def get_store():
    store = IOMemory()
    for alias, ns in NAMESPACES.items():
        store.bind(alias, ns)
    return store


store = get_store()
# print list(store.namespaces())

import json
fn = 'sample.json'
data = json.load(open(fn, 'rb'))

graph = Graph(store, identifier=URIRef('urn:%s' % fn))
for person in data.get('persons'):
    id = URIRef('urn:' + person['id'])
    for k, p in Person.__dict__.items():
        if isinstance(p, URIRef) and k in person:
            v = person.get(k)
            if not isinstance(v, (dict, tuple, list)):
                graph.add((id, p, Literal(v)))
            # print k, v

# print dir(Person), Person.__dict__

cg = ConjunctiveGraph(store)
print(cg.serialize(format='nquads'))
