import requests
import re
import json
from bs4 import BeautifulSoup

# Contributors
#  Ben Varian 23215049
#  Mitchell Otley 23475725


def get_contact(html):
    weekly_keywords = [
        "PER WEEK",
        "WEEKLY",
        "LECTURE",
        "WORKSHOP",
        "TUTORIAL",
        "SEMINAR",
    ]
    classes = {}
    contact_list = html.find_all("br")
    if not contact_list:  # no <i> flag inside html string
        for d, h in list(zip(contact_list, re.findall(r"(\d+)",
                                                      html.get_text()))):
            if any(keyword in d.getText().upper() for keyword
                   in weekly_keywords):
                classes[d.getText()] = int(h) * 12
            else:
                classes[d.getText()] = int(h)
    else:
        contact_list = [i.find_previous() for i in contact_list]
        # If there is a set of hours in the format 'a x b' hours
        for d, h in list(
            zip(contact_list, re.findall(r"(\d+\s*x\s*\d+)", html.get_text()))
        ):
            if any(keyword in d.getText().upper() for keyword
                   in weekly_keywords):
                semester_hours = int(h[0]) * int(h[-1]) * 12
                classes[d.getText()] = semester_hours
                # print(d.getText(), semester_hours)
            else:
                semester_hours = int(h[0]) * int(h[-1])
                classes[d.getText()] = semester_hours
        # If there is a set of hours in the format 'a hours'
        for d, h in list(zip(contact_list, re.findall(r"(\d+)",
                                                      html.get_text()))):
            if d.getText() not in classes:
                if (
                    any(keyword in d.getText().upper() for keyword
                        in weekly_keywords)
                    and int(h) <= 5
                ):
                    hours = int(h) * 12
                    classes[d.getText()] = hours
                    # print(d.getText(), int(h)*12)
                else:
                    classes[d.getText()] = int(h)
                    # print(d.getText(), int(h))

    # Sum all hours to get semester contact hours
    sum = 0
    for value in classes.values():
        sum += value

    return sum


# set url and headers
url = "https://handbooks.uwa.edu.au/unitdetails?code="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
}

unit_code = []

# reading in majors
code = open("majors.json", "r")
dump = json.load(code)
code.close()

for i in dump.items():
    for level in range(1, 5):
        key = f"Level{level}Units"
        for unit in i[1][key]:
            if unit not in unit_code:
                unit_code.append(unit)


# the unit currently being crawled
# code = codes.readline().strip()

# the dictionary of units.
units = {}

for code in unit_code:
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
                for h, d in list(zip(value.find_all("thead th"),
                                     row.find_all("td"))):
                    offer[h.get_text().strip()] = d.get_text().strip()
            unit[key] = offer
        # Find Majors in which the course appears (note, only name, not code is
        # given.
        elif key == "Details for undergraduate courses":
            majors = value.find("li").get_text().strip()
            unit["Majors"] = re.findall(r"([A-Z][^;]*)", majors[5:-16])
        # Extract list of outcomes using a regexp
        elif key == "Outcomes":
            outcomes = value.get_text().strip()
            outcomes = re.findall(r"\d\)([^\(;]*)", outcomes)
            unit[key] = [outcome.strip().capitalize() for outcome in outcomes]
        # Extract description of assessment items
        elif key == "Assessment":
            assessments = value.get_text().strip()
            assessments = re.findall(r"\d\)([^\(;.]*)", assessments)
            unit[key] = [assessment.strip().capitalize() for assessment
                         in assessments]
        # find Unit Coordinator name
        elif key == "Unit Coordinator":
            unit[key] = value.get_text().strip()
        # find description of contact hours with class type and time per week
        elif key == "Contact hours":
            classes = get_contact(value)
            unit[key] = classes

        # find prerequisites. Format is vague, should probably convert to CNF.
        # deeply unsatisfactory. Should aim to capture the Boolean rules here.
        # Will accept as disjunct.
        elif key == "Unit rules":
            for k, v in list(zip(value.find_all("dt"), value.find_all("dd"))):
                prereqs = list(map(lambda x: x.get_text().strip(),
                                   v.find_all("a")))
                cleaned_prereqs = []
                for prereq in prereqs:
                    if (
                        re.search("[A-Z]{4}\d{4}$", prereq) is not None
                        and len(prereq) == 8
                    ):
                        cleaned_prereqs.append(prereq)
                    else:
                        pass
                if cleaned_prereqs:
                    unit[k.get_text().strip()] = cleaned_prereqs
        # textbooks
        elif key == "Texts":
            texts = list(
                map(lambda x: x.get_text().strip().capitalize(),
                    value.find_all("p"))
            )
            for text in texts.copy():
                if text == "":
                    texts.remove(text)
            if texts:
                unit[key] = texts
    units[code] = unit
    # code = codes.readline().strip()


out = open("units.json", "w")
# write to file with indent set to 4.
json.dump(units, out, indent=4)
