from pyshacl import validate
from pathlib import PurePath

# 40 contact hours per week
# 40 * 12 = 480 per semester

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