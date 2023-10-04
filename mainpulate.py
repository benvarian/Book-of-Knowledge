import json
import re

with open("datafile.json", "r") as outfile:
    file = json.load(outfile)
    for code in file.items():
        newstring = code[1]["Outcomes"].replace("Students are able to ", "")
        pattern = r"\(\d+\)"
        num_matches = re.findall(pattern, newstring)
        text_list = []
        print(f"{newstring} {len(num_matches)} \n\n")
