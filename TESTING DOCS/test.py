from owlready2 import *
onto_path.append("./")
onto = get_ontology("http://test.org/onto.owl#")

with onto:

    class Bacterium(Thing):
        pass

    class Shape(Thing):
        pass

    class Grouping(Thing):
        pass

    class Rod(Shape):
        pass

    class Isolated(Grouping):
        pass

    class inPair(Grouping):
        pass

    class has_shape(Bacterium >> Shape, FunctionalProperty):
        pass

    class has_grouping(Bacterium >> Grouping):
        pass

    class gram_positive(Bacterium >> bool, FunctionalProperty):
        pass

    class has_rare_shape(has_shape):
        pass

isolated = Isolated()
my_bacterium = Bacterium(
    "my_bacterium", gram_positive=True, has_shape=Rod(),
    has_grouping=[isolated]
)
my_bacterium.has_grouping.append(inPair())
print(my_bacterium.has_grouping)
onto.save()