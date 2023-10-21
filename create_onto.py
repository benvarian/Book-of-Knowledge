from owlready2 import (
    get_ontology,
    Thing,
    ObjectProperty,
    FunctionalProperty,
    TransitiveProperty,
    Or,
    DataProperty,
    Imp
)


onto = get_ontology("http://test.org/handbook.owl/")

# Add to ontology
with onto:
    class Major(Thing):
        pass

    class Unit(Thing):
        pass

    class Outcome(Thing):
        pass

    class Text(Thing):
        pass

    class has_level_one_units(Major >> Unit):
        pass

    class has_level_two_units(Major >> Unit):
        pass

    class has_level_three_units(Major >> Unit):
        pass

    class has_level_four_units(Major >> Unit):
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

    class has_pre_requisites(Unit >> Unit, TransitiveProperty):
        pass

    class has_credit_points(Unit >> int, FunctionalProperty):
        pass

    class has_level(Unit >> int, FunctionalProperty):
        pass

    class has_assessment(Unit >> str):
        pass

    class has_contact_hours(Unit >> int, FunctionalProperty):
        pass

    class has_text(Or([Major, Unit]) >> Text):
        pass

    outcome_axiom1 = Imp()
    outcome_axiom1.set_as_rule(
        "has_level_one_units(?m, ?u), has_outcome(?u, ?o) -> has_outcome(?m, ?o)"
        )
    
    outcome_axiom2 = Imp()
    outcome_axiom2.set_as_rule(
        "has_level_two_units(?m, ?u), has_outcome(?u, ?o) -> has_outcome(?m, ?o)"
        )
    
    outcome_axiom3 = Imp()
    outcome_axiom3.set_as_rule(
        "has_level_three_units(?m, ?u), has_outcome(?u, ?o) -> has_outcome(?m, ?o)"
        )
    
    outcome_axiom4 = Imp()
    outcome_axiom4.set_as_rule(
        "has_level_four_units(?m, ?u), has_outcome(?u, ?o) -> has_outcome(?m, ?o)"
        )
    
    text_axiom1 = Imp()
    text_axiom1.set_as_rule(
        "has_level_one_units(?m, ?u), has_text(?u, ?t) -> has_text(?m, ?t)"
    )

    text_axiom2 = Imp()
    text_axiom2.set_as_rule(
        "has_level_two_units(?m, ?u), has_text(?u, ?t) -> has_text(?m, ?t)"
    )

    text_axiom3 = Imp()
    text_axiom3.set_as_rule(
        "has_level_three_units(?m, ?u), has_text(?u, ?t) -> has_text(?m, ?t)"
    )

    text_axiom4 = Imp()
    text_axiom4.set_as_rule(
        "has_level_four_units(?m, ?u), has_text(?u, ?t) -> has_text(?m, ?t)"
    )

onto.save(file="handbook.owl")
