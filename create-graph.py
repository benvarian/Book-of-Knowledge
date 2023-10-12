from rdflib import Graph, Namespace, Literal, RDF
import json

uwa = Graph()

unit = Namespace("https://uwa.handbook/unit/")
major = Namespace("https://uwa.handbook/major/")

uwa.bind("unit", unit)
uwa.bind("major", major)


with open("./majors.json", "r") as file:
    major_dump = json.load(file)
with open("./units.json", "r") as file:
    unit_dump = json.load(file)

for major in major_dump.keys():
    print(major)
for unit in unit_dump.keys():
    print(unit)
print("Done")