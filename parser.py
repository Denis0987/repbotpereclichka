import requests
from bs4 import BeautifulSoup
import json

from secrets import cookies

def checkPresent():
    URL = "https://up.omgtu.ru/index.php?r=journal/index"

    with open("present_names.json", encoding='utf-8') as f:
        people = [name.upper() for name in json.load(f)]

    values = dict()

    with requests.Session() as s:
        r = s.get(URL, cookies=cookies)

        soup = BeautifulSoup(r.text, "html.parser")
        block = soup.find(class_="bs-docs-section")
        date = block.find(class_="active").get_text().strip()
        print(date, "\n")

        table = block.tbody
        table_rows = table.find_all("tr")

        for row in table_rows:
            name = row.th.get_text().upper()
            for person in people:
                if person == name:
                    columns = row.find_all("td")
                    for col in columns:
                        if bool(col.find_all()):
                            val = col.find("select")["name"]
                            values[val] = 1

    r = requests.post(URL, data=values, cookies=cookies)
    print(r)
