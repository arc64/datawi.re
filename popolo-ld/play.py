from rdflib import Dataset, Literal, URIRef, Namespace
from rdflib import ConjunctiveGraph, Graph, BNode
from rdflib.plugins.memory import IOMemory
from rdflib.namespace import DC, FOAF, OWL


attrs = Namespace('http://api.datawi.re/attributes/')
default_ctx = URIRef('http://api.datawi.re')
store = IOMemory()
store.bind('attrs', attrs)

bn = URIRef('mailto:friedrich@pudo.org')
ig = Graph(store, identifier=default_ctx)
# ig.bind('attr', attrs)
# ig.add((bn, attrs.label, Literal('Test of the thing')))

# context = {'x': types}
# print('-' * 72)
# print(g.serialize(format='turtle', indent=2))

other_ctx = URIRef('urn:fucked')
xg = Graph(store, identifier=other_ctx)
# g.default_context = Graph(identifier=URIRef('http://api.datawi.re'))
# g.bind('types', types)
# xg.add((bn, attrs.label, Literal('Test of the thing')))


a = URIRef('http://pudo.org/test')
xg.add((a, DC.title, Literal('Test value')))

b = URIRef('http://datawi.re/test')
ig.add((b, DC.author, Literal('Friedrich Lindenberg')))
ig.add((b, OWL.sameAs, a))

ng = ConjunctiveGraph(store)
# print dir(ng)
# ng += ig
# ng += xg

# from RDFClosure import DeductiveClosure, OWLRL_Semantics
# closure = DeductiveClosure(OWLRL_Semantics,
#                            rdfs_closure=False,
#                            axiomatic_triples=False,
#                            datatype_axioms=False)
# closure.expand(ng)

print(ng.serialize(format='nquads'))
# print(ng.serialize(format='n3', indent=2))

# context = {'attrs': attrs, 'dc': DC, 'owl': OWL}
# print(ng.serialize(format='json-ld', context=context, indent=2))


def graph_to_popolo(graph):
    pass


def popolo_to_graph(data):
    pass


class Searcher(object):
    pass


class Result(object):

    def transform():
        pass

    def score():
        pass


x = URIRef('urn:foo')
# x.__slots__ = ('name',)
# x.name = 'foo'
# print dir(x), x.title()
