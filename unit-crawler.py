import requests
import lxml
import re
import json
from bs4 import BeautifulSoup

# set url and headers
url = "https://handbooks.uwa.edu.au/unitdetails?code="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
}

# unit codes is a textfile containing the 8 character unit codes, 1 to a line.
# test only with small lists of units (e.g. CITS units)
codes = open("unit-codes.txt", "r")

# the unit currently being crawled
code = codes.readline().strip()

# the dictionary of units.
units = {}

while code:
    print(code)
    page = requests.get(url + code, headers=headers)

    soup = BeautifulSoup(page.content, "lxml")
    # put all data into units dictionary

    # specify code
    unit = {"code": code}
    # take title (dropping off code at the end)
    unit["title"] = soup.find(id="pagetitle").get_text().strip()[0:-11]
    # assume unit level is implicit in the code
    unit["level"] = code[4]

    # Assume the relevant fields are contained in dictionary lists
    # (which is mostly true).
    for key, value in list(zip(soup.find_all("dt"), soup.find_all("dd"))):
        key = key.get_text().strip()
        # Description is a text file (html characters are stripped out)
        if key == "Description":
            unit[key] = value.get_text()
        # credit is a number (remove "points")
        elif key == "Credit":
            unit[key] = value.get_text().strip()[0:-7]
        # correct? doesn't seem to be widely used?
        elif key == "Offering":
            offer = {}
            for row in value.find_all("tbody tr"):
                for h, d in list(zip(value.find_all("thead th"), row.find_all("td"))):
                    offer[h.get_text().strip()] = d.get_text().strip()
            unit[key] = offer
        # Find Majors in which the course appears (note, only name, not code is given.
        elif key == "Details for undergraduate courses":
            majors = value.find("li").get_text().strip()
            unit["Majors"] = re.findall(r"([A-Z][^;]*)", majors[5:-16])
        # Extract list of outcomes using a regexp
        elif key == "Outcomes":
            outcomes = value.get_text().strip()
            unit[key] = re.findall(r"\d\)([^\(;]*)", outcomes)
        # Extract description of assessment items
        elif key == "Assessment":
            assessments = value.get_text().strip()
            unit[key] = re.findall(r"\d\)([^\(;.]*)", assessments)
        # find Unit Coordinator name
        elif key == "Unit Coordinator":
            unit[key] = value.get_text().strip()
        # find description of contact hours with class type and time per week (working?)
        elif key == "Contact Hours":
            classes = {}
            for d, h in list(
                zip(value.find_all("i"), re.findall(r"(\d)", value.get_text()))
            ):
                classes[desc[i]] = classes[hours[i]]
            unit["Contact"] = classes
        # find prerequisites. Format is vague, should probably convert to CNF.
        elif (
            key == "Unit rules"
        ):  # deeply unsatisfactory. Should aim to capture the Boolean rules here. Will accept as disjunct.
            for k, v in list(zip(value.find_all("dt"), value.find_all("dd"))):
                unit[k.get_text().strip()] = list(
                    map(lambda x: x.get_text().strip(), v.find_all("a"))
                )
        # textbooks
        elif key == "Texts":
            texts = list(map(lambda x: x.get_text().strip(), value.find_all("p")))
    units[code] = unit
    code = codes.readline().strip()

codes.close()
out = open("units.json", "w")
# write to file with indent set to 2.
json.dump(units, out, indent=2)
