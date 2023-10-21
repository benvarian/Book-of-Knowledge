from owlready2 import (
    get_ontology,
    sync_reasoner,
    sync_reasoner_pellet
)
import json


def extract_units(list_of_units):
    units = []
    for unit in list_of_units:
        units.append(onto.Unit(unit))
    return units

onto = get_ontology("./handbook.owl")
loaded = onto.load()

## Load Knowledge Graph into ontology
with open("majors.json", "r") as file:
    majors = json.load(file)

with open("units.json", "r") as output:
    units = json.load(output)

for unit in units.items():
    prereqs = extract_units(unit[1].get("Prerequisites", ""))
    contact_hours = unit[1].get('Contact hours')
    outcomes = []
    for outcome in unit[1]["Outcomes"]:
        outcomes.append(onto.Outcome(outcome.replace(" ", "_").replace("\n", "_")))
    unit_mod = onto.Unit(unit[0])
    for outcome in outcomes:
        unit_mod.has_outcome.append(outcome)
    unit_mod.has_name=unit[1]["title"].replace(" ", "_")
    unit_mod.has_credit_points=int(unit[1]["Credit"])
    unit_mod.has_description=unit[1]["Description"].replace(" ", "_")
    unit_mod.has_level=int(unit[1]["level"])
    
    unit_mod.has_pre_requisites=prereqs
    unit_mod.has_assessment=unit[1]["Assessment"]
    unit_mod.has_contact_hours=contact_hours
    

for major in majors.items():
    units_level_one = extract_units(major[1]["Level1Units"])
    units_level_two = extract_units(major[1]["Level2Units"])
    units_level_three = extract_units(major[1]["Level3Units"])
    name = major[1]["Name"].replace(" ", "_")
    desc = major[1]["Description"].replace(" ", "_")
    
    major_owl = onto.Major(
        major[0],
        has_level_one_units=units_level_one,
        has_level_two_units=units_level_two,
        has_level_three_units=units_level_three,
        has_name=name,
        has_description=desc
    )

    out = [onto.Outcome(out.replace(" ", "_").replace("\n", "_")) for out in major[1]["Outcomes"]]
    major_owl.has_outcome.extend(out)

sync_reasoner(onto, infer_property_values=True)
    
onto.save("handbook_populated.owl")

# ## Test Prerequisite of a Prerequisite
# units = onto.Unit.instances()

# for unit in units:
#     direct_prereqs = unit.has_pre_requisites
#     # print(f"{unit} Direct prerequisites: {direct_prereqs}")

#     all_prereqs = unit.INDIRECT_has_pre_requisites
#     indirect_prereqs = []
#     for prereq in all_prereqs:
#         if prereq not in direct_prereqs:
#             indirect_prereqs.append(prereq)
#     # print(f"{unit} Indirect prerequisites: {indirect_prereqs}\n")



# ## Test Outcome of a Unit is Outcome of a Major
# majors = onto.Major.instances()
# for major in majors:
#     direct_outcomes = major.has_outcome
#     print(f"\n{major} Direct Outcomes:")
#     for outcome in direct_outcomes: print(f"\t{outcome}")

#     all_outcomes = major.INDIRECT_has_outcome
#     indirect_outcomes = []
#     for outcome in all_outcomes:
#         if outcome not in direct_outcomes:
#             indirect_outcomes.append(outcome)
#     print(f"{major} Indirect Outcomes:")
#     for outcome in indirect_outcomes: print(f"\t{outcome}")
