from pyshacl import validate
from pathlib import PurePath

if(__name__ == "__main__"):
    # Assuming graph in same directory
    handbook = str(PurePath("handbook.ttl"))
    shacl_file = str(PurePath("shacl_constraints.ttl"))

    conforms, v_graph, v_text = validate(data_graph=handbook,
                                        shacl_graph=shacl_file,
                                        inference='rdfs',
                                        serialize_report_graph=True)

    print(conforms)
    print(v_text)
    filename = "validation_results.ttl"
    with open(filename, 'w') as file:
        file.write(v_graph.decode())
        print(f"Validation Graph written to file {filename}")