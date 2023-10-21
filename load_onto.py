from owlready2 import get_ontology, sync_reasoner_pellet
import json
import re

# Contributors
#  Ben Varian 23215049
#  Mitchell Otley 23475725


# Function to convert a list of unit codes
# from a string to the ontology Unit class
def extract_units(list_of_units):
    units = []
    for unit in list_of_units:
        units.append(onto.Unit(unit))
    return units


onto = get_ontology("./handbook.owl")
loaded = onto.load()

# Load Data into ontology
with open("scraping_results/majors.json", "r", encoding='utf-8') as file:
    majors = json.load(file)

with open("scraping_results/units.json", "r", encoding='utf-8') as output:
    units = json.load(output)


# Add Units to ontology
for unit in units.items():
    # Extract Data
    prereqs = extract_units(unit[1].get("Prerequisites", ""))
    outcomes = []
    for outcome in unit[1]["Outcomes"]:
        outcomes.append(onto.Outcome(outcome.replace(" ", "_").replace("\n",
                                                                       "_")))
    texts = [
        onto.Text(text.replace(" ", "_").replace("\n", "_"))
        for text in unit[1].get("Texts", "")
    ]
    name = re.sub(r"[ ']", "_", str(unit[1]["title"]))
    name = re.sub(r"[\u0080-\uffff]", "_", name)
    desc = re.sub(r"['\t\\\n\r\"]", "", str(unit[1]["Description"]))
    desc = re.sub(r"[\u0080-\uffff]", "_", desc)
    assessments = [str(assessment.replace("—", "").replace("–", "").replace("\n", "").replace("'", "")) for assessment in unit[1]["Assessment"]]
    
    # Add unit to ontology
    unit_mod = onto.Unit(
        unit[0],
        has_name=name,
        has_description=desc,
        has_credit_points=int(unit[1]["Credit"]),
        has_pre_requisites=prereqs,
        has_assessment=assessments,
        has_contact_hours=unit[1].get("Contact hours"),
        has_outcome=outcomes,
        has_text=texts,
    )

# Add majors to ontology
for major in majors.items():
    # Extract data
    units_level_one = extract_units(major[1]["Level1Units"])
    units_level_two = extract_units(major[1]["Level2Units"])
    units_level_three = extract_units(major[1]["Level3Units"])
    units_level_four = extract_units(major[1].get("Level4Units", ""))
    name = str(major[1]["Name"].replace(" ", "_").replace("'", ""))
    name = re.sub(r"[ ']", "_", str(major[1]["Name"]))
    name = re.sub(r"[\u0080-\uffff]", "_", name)
    desc = re.sub(r"['\t\\\n\r\"]", "", str(unit[1]["Description"]))
    desc = re.sub(r"[\u0080-\uffff]", "_", desc)

    # Add major and its details to ontology
    major_owl = onto.Major(
        major[0],
        has_level_one_units=units_level_one,
        has_level_two_units=units_level_two,
        has_level_three_units=units_level_three,
        has_level_four_units=units_level_four,
        has_name=name,
        has_description=desc,
    )

    outcomes = [
        onto.Outcome(out.replace(" ", "_").replace("\n", "_"))
        for out in major[1]["Outcomes"]
    ]
    major_owl.has_outcome.extend(outcomes)

sync_reasoner_pellet(onto, infer_property_values=True, infer_data_property_values=True, debug=2)

onto.save("handbook_populated.owl")
