import requests
import lxml
import re
import json
from bs4 import BeautifulSoup

# set url and headers
url = "https://handbooks.uwa.edu.au/majors"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"
}

majors = {}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "lxml")
major_div = soup.find('div', {'class': 'folio-device folio-accordion'})

majors = major_div.find_all('li')
major_dict = {}
for major in majors:
    id = major.contents[1].replace('[', '').replace(']', '').strip()
    major_dict[id] = {}


base = "https://handbooks.uwa.edu.au/majordetails?code="
for major in major_dict.keys():
    # Get link to major
    link = base + major
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    # Description
    desc = soup.find('dt', string="Description")
    desc = desc.findNext('p')
    if(len(desc.text) == 0): 
        desc = desc.findNext('p').getText(separator="")
    else:
        desc = desc.getText(separator="")
    major_dict[major]["Description"] = desc
    # Outcomes
    outcomes = soup.find('dt', string="Outcomes")
    outcomes = outcomes.findNext('p').getText(separator="")
    major_dict[major]["Outcomes"] = outcomes
    # Prerequisites
    prereq = soup.find('dt', string="Prerequisites")
    prereq = prereq.findNext('p').getText(separator="")
    major_dict[major]["Prerequisites"] = prereq
    # First Year Units
    y1 = soup.find('h4', {'id':"dsmlevel1"})
    y1codes = []
    if(y1):
        y1 = y1.findNext('tbody')
        y1 = y1.findChildren(name='td')
        for line in y1:
            if(line.find('a', recursive=False)):
                y1codes.append(line.getText(separator=""))
    major_dict[major]["Level1Units"] = y1codes
    # Second Year Units
    y2 = soup.find('h4', {'id':"dsmlevel2"})
    y2codes = []
    if(y2):
        y2 = y2.findNext('tbody')
        y2 = y2.findChildren(name='td')
        
        for line in y2:
            if(line.find('a', recursive=False)):
                y2codes.append(line.getText(separator=""))
    major_dict[major]["Level2Units"] = y2codes
    # Third Year Units
    y3 = soup.find('h4', {'id':"dsmlevel3"})
    y3codes = []
    if(y3):
        y3 = y3.findNext('tbody')
        y3 = y3.findChildren(name='td')
        for line in y3:
            if(line.find('a', recursive=False)):
                y3codes.append(line.getText(separator=""))
    major_dict[major]["Level3Units"] = y3codes
    # Fourth Year Units
    y4 = soup.find('h4', {'id':"dsmlevel4"})
    y4codes = []
    if(y4):
        y4 = y4.findNext('tbody')
        y4 = y4.findChildren(name='td')
        for line in y4:
            if(line.find('a', recursive=False)):
                y4codes.append(line.getText(separator=""))
    major_dict[major]["Level4Units"] = y4codes

with open("datafile.json", "w") as file:
    json.dump(major_dict, file, indent=4)
