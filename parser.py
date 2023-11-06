import requests
from bs4 import BeautifulSoup
import json
from auth import get_cockies


def checkPresent():
    get_cockies()
    URL = "https://up.omgtu.ru/index.php?r=journal/index"

    with open("present_names.json", 'r', encoding='utf-8') as f:
        # people = [name.upper() for name in json.load(f)]
        people = json.load(f)
    values = dict()
    arr_selected_value = []

    for count_value in people:
        arr_selected_value.append(people[count_value])
    print(arr_selected_value)

    with requests.Session() as s:
        with open("cookie.json", 'r', encoding='utf-8') as f:
            # people = [name.upper() for name in json.load(f)]
            cookies = json.load(f)
        print(cookies)
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
                if person.upper() == name:
                    columns = row.find_all("td")
                    for col in columns:
                        if bool(col.find_all()):
                            if(people[person] == 1):
                                val = col.find("select")["name"]
                                values[val] = 1
                            elif(people[person] == 4):
                                val = col.find("select")["name"]
                                values[val] = 2
                            elif (people[person] == 5):
                                val = col.find("select")["name"]
                                values[val] = 4
    r = requests.post(URL, data=values, cookies=cookies)
    print(r)
