import time

from selenium import webdriver
from time import sleep
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


def get_cockies():
    cookie={}
    s = Service(executable_path='geckodriver.exe',
                log_output='geckodriver.log')

    options = Options()
    options.add_argument("--headless")

    data = {
        'login': "Denis_Ivanov_8032",
        'password': "11800cce",
        'name': "Денис",
        'surname': "Иванов",
        'email': "Denis8.9@bk.ru",
    }

    ready_cockie = ""

    with (webdriver.Firefox(service=s, options=options) as driver):
        driver.get("https://omgtu.ru/ecab/")
        driver.find_element(By.XPATH, "//input[@name='USER_NAME']").send_keys(data.get('name'))
        driver.find_element(By.XPATH, "//input[@name='USER_LAST_NAME']").send_keys(data.get('surname'))
        driver.find_element(By.XPATH, "//input[@name='USER_EMAIL']").send_keys(data.get('email'))
        driver.find_element(By.XPATH, "//input[@name='USER_LOGIN']").send_keys(data.get('login'))
        driver.find_element(By.XPATH, "//input[@name='USER_PASSWORD']").send_keys(data.get("password"))
        #wait = WebDriverWait(driver, 5)
        #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[onclick*="$(\'#abitloginform\').submit();"]'))).click()
        driver.find_element(By.CSS_SELECTOR, 'div[onclick*="$(\'#abitloginform\').submit();').click()
        driver.find_element(By.XPATH, "//a[@href='/ecab/up.php?student=1']").click()
        driver.get("https://up.omgtu.ru/index.php?r=journal/index")
        driver.find_element(By.XPATH, "//a[@class='dropdown-toggle']").click()
        driver.find_element(By.XPATH, "//a[@href='/index.php?r=journal/index']").click()
        all_cock = [driver.get_cookies()]
        print(all_cock)
        for j in all_cock[-1]:
            if j.get('name') == "STUDSESSID":
                ready_cockie += (j.get("value"))
                break
        else:
            print("Куки не найдены")
        #driver.close()
        with open("cookie.json", "w", encoding="utf-8") as f:
            cookie["STUDSESSID"] = ready_cockie
            json.dump(cookie, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_cockies()
