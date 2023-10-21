from rdflib import Graph, Namespace, Literal, RDF, URIRef
import json

g = Graph()

uwa = Namespace("https://uwa.handbook/")
code = Namespace("https://uwa.handbook/code/")
rel = Namespace("https://uwa.handbook/relation/")

major_type = uwa["major"]
unit_type = uwa["unit"]

# Major-specific relations
name =  rel["Name"]
l1unit = rel["L1Unit"]
l2unit = rel["L2Unit"]
l3unit = rel["L3Unit"]
l4unit = rel["L4Unit"]

# Unit-specific relations
title =      rel["Title"]
credit =     rel["Credit"]
level =      rel["Level"]
assess =     rel["Assessment"]
in_major =   rel["inMajor"]
contact =    rel["ContactHours"]
coreq =      rel["Corequisite"]
incomp =     rel["Incompatability"]
priorStudy = rel["AdvisablePriorStudy"]
text =      rel["Texts"]

# Major and units relations
outcome = rel["Outcome"]
desc =    rel["Description"]
prereq =  rel["Prerequisite"]


g.bind("uwa", uwa)
g.bind("code", code)
g.bind("rel", rel)


# Majors
with open("./majors.json", "r") as file:
    major_dump = json.load(file)


for instance in major_dump.items():
    major_URI = code[instance[0]]
    g.add((major_URI, RDF.type, major_type))
    if('Name' in instance[1]):
        g.add((major_URI, name, Literal(instance[1]['Name'])))
    if('Description' in instance[1]):
        g.add((major_URI, desc, Literal(instance[1]['Description'])))
    if('Outcomes' in instance[1]):
        for string in instance[1]['Outcomes']:
            g.add((major_URI, outcome, Literal(string)))
    if('Prerequisites' in instance[1]):
        g.add((major_URI, prereq, Literal(instance[1]['Prerequisites'])))
    if('Level1Units' in instance[1]):
        for i in instance[1]['Level1Units']:
            g.add((major_URI, l1unit, code[i]))
    if('Level2Units' in instance[1]):
        for i in instance[1]['Level2Units']:
            g.add((major_URI, l2unit, code[i]))
    if('Level3Units' in instance[1]):
        for i in instance[1]['Level3Units']:
            g.add((major_URI, l3unit, code[i]))
    if('Level4Units' in instance[1]):
        for i in instance[1]['Level4Units']:
            g.add((major_URI, l4unit, code[i]))


# Units
with open("./units.json", "r") as file:
    unit_dump = json.load(file)

for instance in unit_dump.items():
    unit_URI = code[instance[0]]
    g.add((unit_URI, RDF.type, unit_type))
    if('title' in instance[1]):
        g.add((unit_URI, title, Literal(instance[1]['title'])))
    if('level' in instance[1]):
        g.add((unit_URI, level, Literal(int(instance[1]['level']))))
    if('Description' in instance[1]):
        g.add((unit_URI, desc, Literal(instance[1]['Description'])))
    if('Credit' in instance[1]):
        g.add((unit_URI, credit, Literal(int(instance[1]['Credit']))))
    if('Majors' in instance[1]):
        for i in instance[1]['Majors']:
            g.add((unit_URI, in_major, Literal(i)))
    if('Outcomes' in instance[1]):
        for i in instance[1]['Outcomes']:
            g.add((unit_URI, outcome, Literal(i.strip().capitalize())))
    if('Assessment' in instance[1]):
        for i in instance[1]['Assessment']:
            g.add((unit_URI, assess, Literal(i.strip().capitalize())))
    if('Prerequisites' in instance[1]):
        for i in instance[1]['Prerequisites']:
            g.add((unit_URI, prereq, code[i]))
    if('Co-requisites' in instance[1]):
        for i in instance[1]['Co-requisites']:
            g.add((unit_URI, coreq, code[i]))
    if('Incompatibility' in instance[1]):
        for i in instance[1]['Incompatibility']:
            g.add((unit_URI, incomp, code[i]))
    if('Advisable prior study' in instance[1]):
        for i in instance[1]['Advisable prior study']:
            g.add((unit_URI, priorStudy, code[i]))
    if('Contact hours' in instance[1]):
        g.add((unit_URI, contact, Literal(int(instance[1]['Contact hours']))))
    if('Texts' in instance[1]):
        for i in instance[1]['Texts']:
            g.add((unit_URI, text, Literal(i)))
    

if(__name__ == "__main__"):
    filename = "handbook.ttl"
    with open(f"{filename}", 'w+') as file:
        serial = g.serialize(format='ttl')
        file.write(serial)
        print(f"Written to file {filename}...")