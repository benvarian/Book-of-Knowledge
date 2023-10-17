from pyshacl import validate
from pathlib import PurePath

# # Contact Hours SPARQL Query equivalent
# query = """
#             Prefix rel: <https://uwa.handbook/relation/>
#             Prefix uwa: <https://uwa.handbook/>
#             Prefix xsd: <http://www.w3.org/2001/XMLSchema>

#             SELECT ?major ?semesters (SUM (?hours) / ?semesters AS ?totalhours)
#             WHERE {
#                 ?major a uwa:major.
#                 OPTIONAL { ?major rel:L4Unit ?any }
#                 BIND(IF(bound(?any), 8, 6) AS ?semesters)
#                 ?major ?level ?unit.
#                 ?unit a uwa:unit.
#                 ?unit rel:ContactHours ?hours.   
#             }
#             GROUP BY ?major
#             HAVING (SUM(?hours) / ?semesters > 40)
# """

if(__name__ == "__main__"):
    # Assuming graph in same directory
    handbook = str(PurePath("handbook.ttl"))
    shacl_file = str(PurePath("handbook-shacl.ttl"))

    conforms, v_graph, v_text = validate(data_graph=handbook,
                                        shacl_graph=shacl_file,
                                        inference='rdfs',
                                        serialize_report_graph=True)

    print(conforms)
    print(v_text)
    with open("validation_results.ttl", 'w') as file:
        file.write(v_graph.decode())