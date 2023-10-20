import owlready2 as owl

onto = owl.get_ontology("http://test.org/onto.owl")

with onto:
    class Person(owl.Thing):
        pass

    class has_brother(owl.ObjectProperty, owl.SymmetricProperty, owl.IrreflexiveProperty):
        domain = [Person]
        range = [Person]
    
    class has_child(Person >> Person):
        pass
    
    class has_uncle(Person >> Person):
        pass

    rule1 = owl.Imp()
    rule1.set_as_rule(
        "has_brother(?p, ?b), has_child(?p, ?c) -> has_uncle(?c, ?b)"
    )

    # This rule gives "irreflexive transitivity",
    # i.e. transitivity, as long it does not lead to has_brother(?a, ?a)"
    rule2 = owl.Imp()
    rule2.set_as_rule(
        "has_brother(?a, ?b), has_brother(?b, ?c), differentFrom(?a, ?c) -> has_brother(?a, ?c)"
    )
    
david = Person("David")
john = Person("John")
pete = Person("Pete")
anna = Person("Anna")
simon = Person("Simon")

owl.AllDifferent([david, john, pete, anna, simon])

david.has_brother.extend([john, pete])

john.has_child.append(anna)
pete.has_child.append(simon)

print("Uncles of Anna:", anna.has_uncle) # -> []
print("Uncles of Simon:", simon.has_uncle) # -> []
owl.sync_reasoner(infer_property_values=True)
print("Uncles of Anna:", anna.has_uncle) # -> [onto.Pete, onto.David]
print("Uncles of Simon:", simon.has_uncle) # -> [onto.John, onto.David]