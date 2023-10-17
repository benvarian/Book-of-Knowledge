from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef

# Create a Graph
g = Graph()

g.parse("handbook.ttl")

# 
                
query = """
            Prefix rel: <https://uwa.handbook/relation/>
            Prefix uwa: <https://uwa.handbook/>
            Prefix xsd: <http://www.w3.org/2001/XMLSchema>

            SELECT ?major ?semesters (SUM (?hours) / ?semesters AS ?totalhours)
            WHERE {
                ?major a uwa:major.
                OPTIONAL { ?major rel:L4Unit ?any }
                BIND(IF(bound(?any), 8, 6) AS ?semesters)
                ?major ?level ?unit.
                ?unit a uwa:unit.
                ?unit rel:ContactHours ?hours.   
            }
            GROUP BY ?major
            HAVING (SUM(?hours) / ?semesters > 40)
"""

qresults = g.query(query)
for line in qresults:
    print(f"{line['major']} - {line['semesters']} - {line['totalhours']}")