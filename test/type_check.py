import unittest

from rdflib import Graph
from rdflib.exceptions import SubjectTypeError
from rdflib.exceptions import PredicateTypeError
from rdflib.exceptions import ObjectTypeError
from rdflib.URIRef import URIRef

foo = URIRef("foo")


class TypeCheckCase(unittest.TestCase):
    backend = 'default'
    path = 'store'

    def setUp(self):
        self.store = Graph(backend=self.backend)
        self.store.open(self.path)

    def tearDown(self):
        self.store.close()

    def testSubjectTypeCheck(self):
        self.assertRaises(SubjectTypeError,
                          self.store.add, (None, foo, foo))

    def testPredicateTypeCheck(self):
        self.assertRaises(PredicateTypeError,
                          self.store.add, (foo, None, foo))

    def testObjectTypeCheck(self):
        self.assertRaises(ObjectTypeError,
                          self.store.add, (foo, foo, None))
