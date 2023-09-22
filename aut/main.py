from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

s = Service(executable_path='geckodriver.exe',
            log_output='geckodriver.log')

# s = Service(executable_path='/home/bunpdy/PycharmProjects/pythonProject/selenium_new/geckodriver')
data = {

    'login': "Denis_Ivanov_8032",
    'password': "11800cce",
    'name': "Денис",
    'surname': "Иванов",
    'email': "Denis8.9@bk.ru",
}

# login = "log"
# password = '123'

with webdriver.Firefox(service=s) as driver:
    driver.maximize_window()
    driver.get("https://omgtu.ru/ecab/")
    sleep(1)
    # sleep(1)
    input_name = driver.find_element(By.XPATH, "//input[@name='USER_NAME']")
    # sleep(1)
    input_name.send_keys(data.get('name'))
    input_surname = driver.find_element(By.XPATH, "//input[@name='USER_LAST_NAME']")
    # sleep(1)
    input_surname.send_keys(data.get('surname'))
    input_email = driver.find_element(By.XPATH, "//input[@name='USER_EMAIL']")
    # sleep(1)
    input_email.send_keys(data.get('email'))
    # sleep(1)
    # # # !
    # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
    #     (By.CSS_SELECTOR, "iframe[src^='https://www.google.com/recaptcha/api2/anchor']")))
    #
    # WebDriverWait(driver, 20).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))).click()
    # sleep(1)
    driver.switch_to.default_content()
    # sleep(1)
    input_log = driver.find_element(By.XPATH, "//input[@name='USER_LOGIN']")
    input_log.send_keys(data.get('login'))
    # sleep(1)
    input_pass = driver.find_element(By.XPATH, "//input[@name='USER_PASSWORD']")
    input_pass.send_keys(data.get("password"))
    sleep(1)
    # !!!
    wait = WebDriverWait(driver, 5)
    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[onclick*="$(\'#abitloginform\').submit();"]')))
    elem = driver.switch_to.active_element
    btn.click()
    # btn_etc = driver.find_element(By.XPATH, "//*[@onclick='$('#abitloginform').submit();']")
    # btn_etc.click()
    # driver.execute_script("arguments[0].scrollIntoView();", btn_etc)
    # actions = ActionChains(driver)
    # actions.move_to_element(btn_etc).perform()
    # sleep(3)
    # actions.move_to_element(btn_etc).perform()
    # sleep(1)
    # btn_etc.click()
    sleep(999999)
