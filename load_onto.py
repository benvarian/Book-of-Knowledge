from owlready2 import (
    get_ontology,
    sync_reasoner_pellet,
    sync_reasoner
)
import json

# Function to convert a list of unit codes
# from a string to the ontology Unit class
def extract_units(list_of_units):
    units = []
    for unit in list_of_units:
        units.append(onto.Unit(unit))
    return units

onto = get_ontology("./handbook.owl")
loaded = onto.load()

## Load Data into ontology
with open("majors.json", "r") as file:
    majors = json.load(file)

with open("units.json", "r") as output:
    units = json.load(output)

for unit in units.items():
    # Extract Data
    prereqs = extract_units(unit[1].get("Prerequisites", ""))
    outcomes = []
    for outcome in unit[1]["Outcomes"]:
        outcomes.append(onto.Outcome(outcome.replace(" ", "_").replace("\n", "_")))
    texts = [onto.Text(text.replace(" ", "_").replace("\n", "_")) for text in unit[1].get("Texts", "")]

    # Add unit to ontology
    unit_mod = onto.Unit(unit[0],
                         has_name=unit[1]["title"].replace(" ", "_"),
                         has_description=unit[1]["Description"].replace(" ", "_"),
                         has_credit_points=int(unit[1]["Credit"]),
                         has_pre_requisites=prereqs,
                         has_assessment=unit[1]["Assessment"],
                         has_contact_hours=unit[1].get('Contact hours'),
                         has_outcome=outcomes,
                         has_text=texts
                         )
    
    

for major in majors.items():
    # Extract data
    units_level_one = extract_units(major[1]["Level1Units"])
    units_level_two = extract_units(major[1]["Level2Units"])
    units_level_three = extract_units(major[1]["Level3Units"])
    units_level_four = extract_units(major[1].get("Level4Units", ""))
    name = major[1]["Name"].replace(" ", "_")
    desc = major[1]["Description"].replace(" ", "_")

    # Add major and its details to ontology
    major_owl = onto.Major(
        major[0],
        has_level_one_units=units_level_one,
        has_level_two_units=units_level_two,
        has_level_three_units=units_level_three,
        has_level_four_units=units_level_four,
        has_name=name,
        has_description=desc
    )

    out = [onto.Outcome(out.replace(" ", "_").replace("\n", "_")) for out in major[1]["Outcomes"]]
    major_owl.has_outcome.extend(out)

sync_reasoner(onto, infer_property_values=True)
    
onto.save("handbook_populated.owl")