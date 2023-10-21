from rdflib import Graph
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

SELECT ?code (COUNT(?Outcome) AS ?count)
WHERE {
?p a uwa:unit.
?p rel:Outcome ?Outcome.
BIND(REPLACE(STR(?p), "https://uwa.handbook/code/", "") AS ?code).
}
GROUP BY ?code
HAVING (COUNT(?Outcome) > 6)
"""
print("--QUERY 1 START--")
for i in g.query(query1):
    count = i["count"]
    code = i["code"]
    print(f"{code},{count}")
print("--QUERY 1 END--\n\n")


# query 2
# Find all level 3 units that do not have an exam,
# and where none of their prerequisites have an exam.
query2 = """
Prefix code: <https://uwa.handbook/code/>
Prefix rel: <https://uwa.handbook/relation/>
Prefix uwa: <https://uwa.handbook/>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?code
WHERE {
  ?unit a uwa:unit.
  ?unit rel:Level ?level.
  ?unit rel:Prerequisite ?prereq.
  ?prereq rel:Title ?prereq_title.
  BIND(REPLACE(STR(?unit), "https://uwa.handbook/code/", "") AS ?code).
  FILTER(?level = 3).
  FILTER NOT EXISTS {
    ?unit rel:Assessment ?assessments.
    FILTER REGEX(?assessments, "exam", "i").
  }
  FILTER NOT EXISTS {
    ?prereq rel:Assessment ?assessments.
    FILTER REGEX(?assessments, "exam", "i").
  }
}
GROUP BY ?code
"""
print("--QUERY 2 START--")
for i in g.query(query2):
    print(i["code"])
print("--QUERY 2 END--\n\n")
# query 3
# Find all units that appear in more than 3 majors.
query3 = """
Prefix code: <https://uwa.handbook/code/>
Prefix rel: <https://uwa.handbook/relation/>
Prefix uwa: <https://uwa.handbook/>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?code (COUNT(?unit) AS ?count)
WHERE {
  {
    ?major a uwa:major.
    ?major ?level ?unit.
    ?unit a uwa:unit.
    BIND(REPLACE(STR(?unit), "https://uwa.handbook/code/", "") AS ?code).
  }
}
GROUP BY ?unit
HAVING (COUNT(?unit) > 3)
"""
print("--QUERY 3 START--")
for i in g.query(query3):
    name = i["code"]
    count = i["count"]
    print(f"{name} appears in {count} majors")
print("--QUERY 3 END--\n\n")
# query 4
# Basic search functionality: Given a query string
# (eg "environmental policy"), can you find the units
# that contain this string in the description or outcomes?
query4 = """
Prefix code: <https://uwa.handbook/code/>
Prefix rel: <https://uwa.handbook/relation/>
Prefix uwa: <https://uwa.handbook/>
Prefix xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?code
WHERE {
?p a uwa:unit.
?p rel:Description ?Description.
?p rel:Outcome ?Outcome.
BIND(REPLACE(STR(?p), "https://uwa.handbook/code/", "") AS ?code).
FILTER(REGEX(?Description, "environmental policy") ||
REGEX(?Outcome, "environmental policy")).
}
"""
print("--QUERY 4 START--")
for i in g.query(query4):
    code = i["code"]
    print(f"{code}")
print("--QUERY 4 END--\n\n")
