from owlready2 import (
    get_ontology,
    Thing,
    onto_path,
    ObjectProperty,
    FunctionalProperty,
    TransitiveProperty,
    Or,
    DataProperty
)
import json

with open("majors.json", "r") as file:
    majors = json.load(file)

with open("units.json", "r") as output:
    units = json.load(output)


onto = get_ontology("http://test.org/handbook.owl/")


def extract_units(list_of_units):
    units = []
    for unit in list_of_units:
        units.append(Unit(unit))
    return units


# Add some majors to the ontology
with onto:
    # classes
    class Major(Thing):
        pass

    class Unit(Thing):
        pass

    class Outcome(Thing):
        pass

    class has_level_one_units(ObjectProperty):
        domain = [Major]
        range = [Unit]

    class has_level_two_units(ObjectProperty):
        domain = [Major]
        range = [Unit]

    class has_level_three_units(ObjectProperty):
        domain = [Major]
        range = [Unit]

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

    for unit in units.items():
        prereqs = extract_units(unit[1].get("Prerequisites", ""))
        contact_hours = unit[1].get('Contact hours')
        unit_mod = Unit(
            unit[0],
            has_name=unit[1]["title"],
            has_credit_points=unit[1]["Credit"],
            has_description=unit[1]["Description"],
            has_outcome=[Outcome(i) for i in unit[1]["Outcomes"]],
            has_level=unit[1]["level"],
            has_pre_requisites=prereqs,
            has_assessment=unit[1]["Assessment"],
            has_contact_hours=contact_hours
        )

    #     level = Level(unit[1]["level"])
    #     credit = Credit(unit[1]["Credit"])
    #     desc = Description(unit[1]["Description"])
    #     outcome = Outcome(handle_outcomes(unit[1]["Outcomes"]))
    #     title = Name(unit[1]["title"])
    #     prereq = extract_units(unit[1].get("Prerequisites", ""))
    #     unit_owl = Unit(
    #         unit[0],
    #         has_name=title,
    #         has_description=desc,
    #         has_outcome=outcome,
    #         has_credit_points=credit,
    #         has_level=level,
    #         has_pre_requisites=prereq,
    #     )
    for major in majors.items():
        units_level_one = extract_units(major[1]["Level1Units"])
        units_level_two = extract_units(major[1]["Level2Units"])
        units_level_three = extract_units(major[1]["Level3Units"])
        name = major[1]["Name"]
        desc = major[1]["Description"]
        outcome = [Outcome(i.strip().capitalize()) for i in major[1]["Outcomes"]]
        major_owl = Major(
            major[0],
            has_level_one_units=units_level_one,
            has_level_two_units=units_level_two,
            has_level_three_units=units_level_three,
            has_name=name,
            has_description=desc,
            has_outcome=outcome
        )


# print(Outcome.__dict__)
# print(unit_owl.__class__)
print(major_owl.__class__)
# print(list(onto.inconsistent_classes()))
onto.save(file="handbook.owl")
