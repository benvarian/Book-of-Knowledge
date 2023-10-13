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
# for i in g.query(query1):
#     title = i["Title"]
#     count = i["count"]
#     print(f"{title}")

# query 2
# Find all level 3 units that do not have an exam,
# and where none of their prerequisites have an exam.
query2 = """
Prefix code: <https://uwa.handbook/code/>
Prefix rel: <https://uwa.handbook/relation/>
Prefix uwa: <https://uwa.handbook/>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>


"""

# query 3
# Find all units that appear in more than 3 majors.
query3 = """
Prefix code: <https://uwa.handbook/code/>
Prefix rel: <https://uwa.handbook/relation/>
Prefix uwa: <https://uwa.handbook/>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>


"""

# query 4
# Basic search functionality: Given a query string
# (eg "environmental policy"), can you find the units
# that contain this string in the description or outcomes?
query4 = """
Prefix code: <https://uwa.handbook/code/>
Prefix rel: <https://uwa.handbook/relation/>
Prefix uwa: <https://uwa.handbook/>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?Title 
WHERE {
?p a uwa:unit.
?p rel:Title ?Title.
?p rel:Description ?Description.
?p rel:Outcome ?Outcome.
FILTER(REGEX(?Description, "environmental policy") ||
REGEX(?Outcome, "environmental policy")).
}
"""
for i in g.query(query4):
    title = i["Title"]
    print(f"{title}")
