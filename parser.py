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
    arr_selected_value = people

    #for count_value in people:
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
        people = people[0]
        print(people)
        for row in table_rows:
            name = row.th.get_text().upper()
            for person in people:
                colcount = 0
                print(person)
                person = person.split("-")
                nameperson = person[0]
                numparperson = int(person[1])
                #if numparperson != 1:
               #     numparperson+=2
                typeparperson = int(person[2])%3
                if nameperson.upper() == name:
                    columns = row.find_all("td")
                    for col in columns:
                        print(colcount, numparperson, typeparperson)
                        if bool(col.find_all()):
                            colcount +=1
                            if colcount == numparperson:
                                    if(typeparperson == 0):
                                        val = col.find("select")["name"]
                                        values[val] = 4
                                    elif(typeparperson == 1):
                                        val = col.find("select")["name"]
                                        values[val] = 1
                                    elif (typeparperson == 2):
                                        val = col.find("select")["name"]
                                        values[val] = 2
    with open("bd_add_user.json", "w") as file:
        file.truncate()
    with open("present_names.json", "w") as file:
        file.truncate()

    r = requests.post(URL, data=values, cookies=cookies)
    print(r)
