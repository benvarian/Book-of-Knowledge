import owlready2 as or2

onto = or2.get_ontology("./majors.owl")
loaded = onto.load()

# Add some majors to the ontology
with onto:
    # classes
    class Major(or2.Thing):
        pass

    class Unit(or2.Thing):
        pass

    class Name(or2.Thing):
        pass

    class Grouping(or2.Thing):
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

    class has_name(Major >> Name, or2.FunctionalProperty):
        pass

    class has_description(Major >> Title, or2.FunctionalProperty):
        pass

    class has_outcome(Major >> Title, or2.FunctionalProperty):
        pass

    class has_pre_requisites(Unit >> Title, or2.TransitiveProperty):
        pass

    class has_credit_points(Unit >> Credit, or2.FunctionalProperty):
        pass

    class has_level(Unit >> Level, or2.FunctionalProperty):
        pass



## Test Prerequisite of a Prerequisite
units = onto.Unit.instances()

for unit in units:
    direct_prereqs = unit.has_pre_requisites
    print(f"{unit} Direct prerequisites: {direct_prereqs}")

    all_prereqs = unit.INDIRECT_has_pre_requisites
    indirect_prereqs = []
    for prereq in all_prereqs:
        if prereq not in direct_prereqs:
            indirect_prereqs.append(prereq)
    print(f"{unit} Indirect prerequisites: {indirect_prereqs}\n")

# ## Test Outcome of a Unit is Outcome of a Major
# majors = onto.Major.instances()

