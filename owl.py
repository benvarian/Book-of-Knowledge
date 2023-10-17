from owlready2 import get_ontology, Thing, onto_path, ObjectProperty, FunctionalProperty
import json

with open("majors.json", "r") as file:
    data = json.load(file)


# onto_path.append("./")
onto = get_ontology("http://test.org/onto.owl#")


def extract_units(list_of_units):
    units = []
    for unit in list_of_units:
        units.append(Unit(unit))
    return units


def handle_outcomes(list_of_outcomes):
    # concat an array of strings into one big one
    main = ""
    for i in list_of_outcomes:
        main += i
    return main

# Add some data to the ontology
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

    class has_level_one_units(Unit >> Title):
        pass

    class has_level_two_units(Unit >> Title):
        pass

    class has_level_three_units(Unit >> Title):
        pass

    class has_name(Major >> Name, FunctionalProperty):
        pass

    class has_description(Major >> Title, FunctionalProperty):
        pass

    class has_outcome(Major >> Title, FunctionalProperty):
        pass

    # class Outcomes(ObjectProperty):
    #     domain = [Major, Unit]

    # class Prerequisites(ObjectProperty):
    #     domain = [Major, Unit]

    # class Level1Unit(Major >> Unit):
    #     domain = [Major]

    # class Level2Unit(ObjectProperty):
    #     domain = [Major]

    # class Level3Unit(ObjectProperty):
    #     domain = [Major]

    # class Level4Unit(ObjectProperty):
    #     domain = [Major]

    # class Code(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]

    # class Title(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]

    # class Level(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]

    # class CreditPoints(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]

    # class Majors(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]

    # class Assessments(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]

    # class Incompatibility(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]

    # class CoRequisites(ObjectProperty):
    #     domain = [Unit]
    #     range = [str]
for major in data.items():
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
        has_outcome=outcome
    )


onto.save(file="majors.owl")
