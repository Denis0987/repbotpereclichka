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
        driver.maximize_window()
        driver.get("https://omgtu.ru/ecab/")
        input_name = driver.find_element(By.XPATH, "//input[@name='USER_NAME']")
        input_name.send_keys(data.get('name'))
        input_surname = driver.find_element(By.XPATH, "//input[@name='USER_LAST_NAME']")
        input_surname.send_keys(data.get('surname'))
        input_email = driver.find_element(By.XPATH, "//input[@name='USER_EMAIL']")
        input_email.send_keys(data.get('email'))
        input_log = driver.find_element(By.XPATH, "//input[@name='USER_LOGIN']")
        input_log.send_keys(data.get('login'))
        input_pass = driver.find_element(By.XPATH, "//input[@name='USER_PASSWORD']")
        input_pass.send_keys(data.get("password"))
        wait = WebDriverWait(driver, 5)
        btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[onclick*="$(\'#abitloginform\').submit();"]')))
        btn.click()
        stud = driver.find_element(By.XPATH, "//a[@href='/ecab/up.php?student=1']")
        stud.click()
        stud = driver.find_element(By.XPATH, "//a[@class='dropdown-toggle']")
        stud.click()
        jurnal = driver.find_element(By.XPATH, "//a[@href='/index.php?r=journal/index']")
        jurnal.click()
        all_cock = [driver.get_cookies()]
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
