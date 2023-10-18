from owlready2 import get_ontology, Thing, onto_path, ObjectProperty, FunctionalProperty
import json

with open("majors.json", "r") as file:
    majors = json.load(file)

with open("units.json", "r") as output:
    units = json.load(output)


onto = get_ontology("http://test.org/onto.owl#")


def extract_units(list_of_units):
    units = []
    for unit in list_of_units:
        units.append(Unit(unit))
    return units


def handle_outcomes(list_of_outcomes):
    main = ""
    for i in list_of_outcomes:
        main += i
    return main


# Add some majors to the ontology
with onto:
    # classes
    class Major(Thing):
        pass

    class Unit(Thing):
        pass

    class Name(Thing):
        pass

    class Grouping(Thing):
        pass

    class Title(Unit):
        pass

    class Description(Major):
        pass

    class Outcome(Major):
        pass

    class Credit(Unit):
        pass

    class Level(Unit):
        pass

    class has_level_one_units(Unit >> Title):
        pass

    class has_level_two_units(Unit >> Title):
        pass

    class has_level_three_units(Unit >> Title):
        pass

    class has_name(FunctionalProperty):
        domain = [Major, Unit]
        range = [Name]

    class has_description(FunctionalProperty):
        domain = [Major, Unit]
        range = [Title]

    class has_outcome(FunctionalProperty):
        domain = [Major, Unit]
        range = [Title]

    class has_pre_requisites(Unit >> Title):
        pass

    class has_credit_points(Unit >> Credit, FunctionalProperty):
        pass

    class has_level(Unit >> Level, FunctionalProperty):
        pass


for major in majors.items():
    units_level_one = extract_units(major[1]["Level1Units"])
    units_level_two = extract_units(major[1]["Level2Units"])
    units_level_three = extract_units(major[1]["Level3Units"])
    name = Name(major[1]["Name"])
    desc = Description(major[1]["Description"])
    outcome = Outcome(handle_outcomes(major[1]["Outcomes"]))
    major_owl = Major(
        major[0],
        has_level_one_units=units_level_one,
        has_level_two_units=units_level_two,
        has_level_three_units=units_level_three,
        has_name=name,
        has_description=desc,
        has_outcome=outcome,
    )
for unit in units.items():
    level = Level(unit[1]["level"])
    credit = Credit(unit[1]["Credit"])
    desc = Description(unit[1]["Description"])
    outcome = Outcome(handle_outcomes(unit[1]["Outcomes"]))
    title = Name(unit[1]["title"])
    prereq = extract_units(unit[1].get("Prerequisites", ""))
    unit_owl = Unit(
        unit[0],
        # has_name=title,
        # has_description=desc,
        # has_outcome=outcome,
        has_credit_points=credit,
        has_level=level,
        has_pre_requisites=prereq,
    )
    # print(unit_owl.domain)


onto.save(file="majors.owl")
