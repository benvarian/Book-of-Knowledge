import owlready2 as or2

onto = or2.get_ontology("./handbook.owl")
loaded = onto.load()

# Add some majors to the ontology
with onto:
    # classes
    class Major(or2.Thing):
        pass

    class Unit(or2.Thing):
        pass

    class Outcome(or2.Thing):
        pass

    class has_level_one_units(or2.ObjectProperty):
        domain = [Major]
        range = [Unit]

    class has_level_two_units(or2.ObjectProperty):
        domain = [Major]
        range = [Unit]

    class has_level_three_units(or2.ObjectProperty):
        domain = [Major]
        range = [Unit]

    class has_name(or2.DataProperty, or2.FunctionalProperty):
        domain = [or2.Or([Major, Unit])]
        range = [str]

    class has_description(or2.DataProperty, or2.FunctionalProperty):
        domain = [or2.Or([Major, Unit])]
        range = [str]

    class has_outcome(or2.FunctionalProperty):
        domain = [or2.Or([Major, Unit])]
        range = [Outcome]

    class has_pre_requisites(Unit >> Unit, or2.ObjectProperty, or2.TransitiveProperty):
        pass

    class has_credit_points(Unit >> int, or2.FunctionalProperty):
        pass

    class has_level(Unit >> int, or2.FunctionalProperty):
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
or2.sync_reasoner()