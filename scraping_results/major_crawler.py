import requests
import re
import json
from bs4 import BeautifulSoup

# Contributors
#  Ben Varian 23215049
#  Mitchell Otley 23475725


# Get the units of a specific level from the html soup
# Return a list of the unit codes
def get_units(soup, level):
    units = soup.find('h4', {'id': f"dsmlevel{level}"})
    yearcodes = []
    if (units):
        units = units.findNext('tbody')
        units = units.findChildren(name='td')
        for line in units:
            if (line.find('a', recursive=False)):
                yearcodes.append(line.getText(separator=""))
    else:
        # EDGE CASE: https://handbooks.uwa.edu.au/majordetails?code=MJS-ARCTB
        # Uses id of smlevel_ instead of dsmlevel_
        units = soup.find('h4', {'id': f"smlevel{level}"})
        if (units):
            units = units.findNext('tbody')
            units = units.findChildren(name='td')
            for line in units:
                if (line.find('a', recursive=False)):
                    yearcodes.append(line.getText(separator=""))
    return yearcodes


# set url and headers
url = "https://handbooks.uwa.edu.au/majors"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
      (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
}

majors = {}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "lxml")
major_div = soup.find('div', {'class': 'folio-device folio-accordion'})

majors = major_div.find_all('li')
major_dict = {}
for major in majors:
    name = major.contents[0].getText()
    id = major.contents[1].replace('[', '').replace(']', '').strip()
    major_dict[id] = {'Name': name}


base = "https://handbooks.uwa.edu.au/majordetails?code="
for major in major_dict.keys():
    # Get link to major
    link = base + major
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    # Description
    desc = soup.find('dt', string="Description")
    desc = desc.findNext('p')
    if (len(desc.text) == 0):
        desc = desc.findNext('p').getText(separator="")
    else:
        desc = desc.getText(separator="")
    major_dict[major]["Description"] = desc
    # Outcomes
    outcomes = soup.find('dt', string="Outcomes")
    outcomes = outcomes.findNext('p').getText(separator="")
    # major_dict[major]["Outcomes"] = outcomes # UNCOMMENT TO ADD OUTCOMES AS
    # ONE STRING

    newstring = outcomes.replace("Students are able to ", "")
    pattern = r"\(\d+\)"
    num_matches = re.findall(pattern, newstring)
    text_list = []
    for i in range(len(num_matches) - 1):
        pattern = rf"\({i+1}\)(.*?)\({i+2}\)"
        match = re.search(pattern, newstring)
        if match:
            text_list.append(match.group(1).strip().capitalize())
    pattern = rf"\({len(num_matches)}\)(.*?)$"
    match = re.search(pattern, newstring)
    if match:
        text_list.append(match.group(1).strip())
    major_dict[major]["Outcomes"] = text_list
    # Prerequisites
    prereq = soup.find('dl', {'class': "columns ruled"})
    prereq = prereq.find(name='dt', string="Prerequisites")
    if (prereq):
        prereq = prereq.find_next(name='p').getText(separator="")
        major_dict[major]["Prerequisites"] = prereq
    # First Year Units
    major_dict[major]["Level1Units"] = get_units(soup, 1)
    # Second Year Units
    major_dict[major]["Level2Units"] = get_units(soup, 2)
    # Third Year Units
    major_dict[major]["Level3Units"] = get_units(soup, 3)
    # Fourth Year Units
    major_dict[major]["Level4Units"] = get_units(soup, 4)

with open("majors.json", "w") as file:
    json.dump(major_dict, file, indent=4)
