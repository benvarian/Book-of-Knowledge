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
    link = base + major
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    desc = soup.find('dt', string="Description")
    desc = desc.findNext('dd').contents[2].contents[0]
    major_dict[major]["Description"] = desc
    outcomes = soup.find('dt', string="Outcomes")
    outcomes = outcomes.findNext('p').contents[0]
    major_dict[major]["Outcomes"] = outcomes

print("done")
