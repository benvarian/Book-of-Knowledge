from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

# Create a Graph
g = Graph()

g.parse("handbook.ttl")

print(g)