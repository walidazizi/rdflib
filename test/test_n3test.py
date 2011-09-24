import os
import sys
import unittest

from rdflib.term import BNode
from rdflib.graph import Graph, ConjunctiveGraph


# TODO: make an introspective version (like this one) of
# rdflib.graphutils.isomorphic and use instead.
def crapCompare(g1, g2):
	"""A really crappy way to 'check' if two graphs are equal. It ignores blank
	nodes completely and ignores subgraphs."""
	if len(g1) != len(g2):
		raise Exception("Graphs dont have same length")
	for t in g1:
		s = _no_blank(t[0])
		o = _no_blank(t[2])
		if not (s, t[1] ,o) in g2:
			e = "(%s, %s, %s) is not in both graphs!"%(s, t[1], o)
			raise Exception(e)
def _no_blank(node):
	if isinstance(node, BNode): return None
	if isinstance(node, Graph):
		return None #node._Graph__identifier = _SQUASHED_NODE
	return node


def check_n3_serialize(filepath, fmt, verbose=False):
	graph = ConjunctiveGraph()
	_parse_or_report(verbose, graph, filepath, format=fmt)
	
	if verbose:
		for t in graph:
			print(t)
		print("========================================")
		print("Parsed OK!")
	
	s = graph.serialize(format='n3')
	
	if verbose:
		print(s)
	
	graph2 = ConjunctiveGraph()
	_parse_or_report(verbose, graph2, data=s, format='n3')
	
	if verbose:
		print(graph2.serialize())
	
	crapCompare(graph,graph2)

def _parse_or_report(verbose, graph, *args, **kwargs):
	try:
		graph.parse(*args, **kwargs)
	except:
		if verbose:
			print("========================================")
			print("Error in parsing serialization:")
			print(args, kwargs)
		raise


def _get_test_files_formats():
	if __name__ == "__main__":
		directory = 'n3/'
	else:
		directory = 'test/n3/'
		
	for f in os.listdir(directory):
		fpath = directory+f
		if f.endswith('.rdf'):
			yield fpath, 'xml'
		elif f.endswith('.n3'):
			yield fpath, 'n3'

def test_all_n3_serialize():
	for fpath, fmt in _get_test_files_formats():
		yield check_n3_serialize, fpath, fmt


if __name__ == "__main__":
	
	class TestN3Writing(unittest.TestCase):
		def testWriting(self):
			for fpath, fmt in _get_test_files_formats():
				check_n3_serialize(fpath, fmt)
	
	if len(sys.argv) > 1:
		check_n3_serialize(sys.argv[1], True)
		sys.exit()
	else:
		unittest.main()

