import unittest

from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib.term import Namespace as NS

from rdflib.sparql import Algebra

from StringIO import StringIO

class TestSparqlASK(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

        io = StringIO("""
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix : <http://goonmill.org/2007/skill.n3#> .

:Foo a rdfs:Class .

:bar a :Foo .
""")

        
        self.graph.load(io, format='n3')

        self.compliance_setting, Algebra.DAWG_DATASET_COMPLIANCE = Algebra.DAWG_DATASET_COMPLIANCE, False

    def tearDown(self):
        Algebra.DAWG_DATASET_COMPLIANCE = self.compliance_setting

    def test_ask_true(self):
        """
        Ask for a triple that exists, assert that the response is True.
        """
        res = self.graph.query('ASK { <http://goonmill.org/2007/skill.n3#bar> a <http://goonmill.org/2007/skill.n3#Foo> } ')
        self.assertEquals(res.askAnswer, [True], "The answer should have been that the triple was found")
 
    def test_ask_false(self):
        """
        Ask for a triple that does not exist, assert that the response is False.
        """
        res = self.graph.query('ASK { <http://goonmill.org/2007/skill.n3#baz> a <http://goonmill.org/2007/skill.n3#Foo> } ')
        self.assertEquals(res.askAnswer, [False], "The answer should have been that the triple was not found")

class TestSparqlASKWithCompliance(TestSparqlASK):
    def setUp(self):
        TestSparqlASK.setUp(self)
        Algebra.DAWG_DATASET_COMPLIANCE = True

if __name__ == "__main__":
    unittest.main()

