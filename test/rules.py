import unittest

from rdflib import *

LOG = Namespace("http://www.w3.org/2000/10/swap/log#")


try:
    from pychinko import terms
    from pychinko.interpreter import Interpreter

    def _convert(node):
        if isinstance(node, Variable):
            return terms.Variable(node)
	    #return node
        elif isinstance(node, BNode):
            return terms.Exivar(node)
        elif isinstance(node, URIRef):
	    #return terms.URI(node)
	    return node
        elif isinstance(node, Literal):
	    return node
	else:
	    raise Exception("Unexpected Type: %s" % type(node))

    def patterns(g):
	for s, p, o in g:
	    yield terms.Pattern(_convert(s), _convert(p), _convert(o))

    def facts(g):
	for s, p, o in g:
	    if p!=LOG.implies and not isinstance(s, BNode) and not isinstance(o, BNode):
		yield terms.Fact(_convert(s), _convert(p), _convert(o))

    class PychinkoTestCase(unittest.TestCase):

	def setUp(self):
	    self.g = Graph()
	    self.g.parse("test/a.n3", format="n3") 
	    print list(self.g)
	
	def tearDown(self):
	    self.g.close()

	def testPychinko(self):
	    rules = []
	    for s, p, o in self.g.triples((None, LOG.implies, None)):
		lhs = list(patterns(s))
		rhs = list(patterns(o))
		rules.append(terms.Rule(lhs, rhs, (s, p, o)))
	    interp = Interpreter(rules)
	    f = Graph()
	    f.parse("http://eikeon.com/")
	    source = f
	    source = self.g
	    interp.addFacts(set(facts(source)), initialSet=True)        
	    interp.run()
	    print interp.inferredFacts

except ImportError, e:
    print "Could not test Pychinko:", e


