from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

# Create a Graph
g = Graph()

g.parse("handbook.ttl")

# query 1
# Find all units with more than 6 outcomes.
query1 = """
Prefix code: <https://uwa.handbook/code/> 
Prefix rel: <https://uwa.handbook/relation/> 
Prefix uwa: <https://uwa.handbook/> 
Prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

SELECT ?Title ?Outcome (COUNT(?Outcome) AS ?count)
WHERE {
?p a uwa:unit.
?p rel:Title ?Title.
?p rel:Outcome ?Outcome.
}
GROUP BY ?Title
HAVING (COUNT(?Outcome) > 6)
"""
for i in g.query(query1):
    title = i["Title"]
    count = i["count"]
    print(f"{title}")

