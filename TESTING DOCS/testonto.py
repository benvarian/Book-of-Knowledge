from owlready2 import (
    get_ontology,
    Thing,
    ObjectProperty,
    FunctionalProperty,
    TransitiveProperty,
    Or,
    DataProperty,
    Imp,
    sync_reasoner,
)
import json


def extract_units(list_of_units):
    units = []
    for unit in list_of_units:
        units.append(onto.Unit(unit))
    return units


onto = get_ontology("http://test.org/handbook.owl/")

# Add to ontology
with onto:

    class Major(Thing):
        pass

    class Unit(Thing):
        pass

    class Outcome(Thing):
        pass

    class has_level_one_units(Major >> Unit):
        pass

    class has_level_two_units(Major >> Unit):
        pass

    class has_level_three_units(Major >> Unit):
        pass

    class has_name(DataProperty, FunctionalProperty):
        domain = [Or([Major, Unit])]
        range = [str]

    class has_description(DataProperty, FunctionalProperty):
        domain = [Or([Major, Unit])]
        range = [str]

    class has_outcome(ObjectProperty):
        domain = [Or([Major, Unit])]
        range = [Outcome]

    class has_pre_requisites(Unit >> Unit, ObjectProperty, TransitiveProperty):
        pass

    class has_credit_points(Unit >> int, FunctionalProperty):
        pass

    class has_level(Unit >> int, FunctionalProperty):
        pass

    class has_assessment(Unit >> str):
        pass

    class has_contact_hours(Unit >> int, FunctionalProperty):
        pass

    axiom = Imp()
    axiom.set_as_rule(
        "has_level_one_units(?m, ?u), has_outcome(?u, ?o) -> \
            has_outcome(?m, ?o)"
    )


with open("majors.json", "r") as file:
    majors = json.load(file)

with open("units.json", "r") as output:
    units = json.load(output)

for unit in units.items():
    outlist = []
    for outcome in unit[1]["Outcomes"]:
        outlist.append(Outcome(outcome.replace(" ", "_")[:30]))
    unit_owl = Unit(unit[0])
    for outcome in outlist:
        unit_owl.has_outcome.append(outcome)


for major in majors.items():
    level_one = extract_units(major[1]["Level1Units"])
    major_owl = Major(major[0], has_level_one_units=level_one)
    # major_owl = Major(major[0], has_level_one_units=[unit, unit2])
    print(f"Outcomes of major: {major_owl.has_outcome}")
    sync_reasoner(onto, infer_property_values=True)
    print(f"Outcomes of major: {major_owl.has_outcome}")

sync_reasoner(onto, infer_property_values=True)
