import requests
from bs4 import BeautifulSoup
import json
import re
from auth import get_cockies

def GainNamePar():
    get_cockies()
    URL = "https://up.omgtu.ru/index.php?r=journal/index"
    sting = []

    with requests.Session() as s:
        with open("cookie.json", 'r', encoding='utf-8') as f:
            # people = [name.upper() for name in json.load(f)]
            cookies = json.load(f)
        r = s.get(URL, cookies=cookies)
        soup = BeautifulSoup(r.text, "html.parser")
        block = soup.find(class_="bs-docs-section")
        date = block.find(class_="active").get_text().strip()
        print(date, "\n")

        thead = block.thead
        table_column = thead.find_all("th", colspan="2")
        for x in range(len(table_column)):
            string = re.sub("([\<]).*?([\>])", "\g<1>\g<2>", str(table_column[x]))
            sting.append(string.split("<>"))
    return (sting)