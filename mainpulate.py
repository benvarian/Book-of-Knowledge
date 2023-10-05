import json
import re

with open("datafile.json", "r") as outfile:
    file = json.load(outfile)
    for code in file.items():
        newstring = code[1]["Outcomes"].replace("Students are able to ", "")
        pattern = r"\(\d+\)"
        num_matches = re.findall(pattern, newstring)
        text_list = []
        for i in range(len(num_matches) - 1):
            pattern = rf"\({i+1}\)(.*?)\({i+2}\)"
            match = re.search(pattern, newstring)
            if match:
                text_list.append(match.group(1).strip())
        pattern = rf"\({len(num_matches)}\)(.*?)$"
        match = re.search(pattern, newstring)
        if match:
            text_list.append(match.group(1).strip())
        code[1]["Outcomes"] = text_list

    with open("datafile_2.json", "w") as outfile:
        json.dump(file, outfile, indent=4)
