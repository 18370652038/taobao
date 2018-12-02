import re
import random
import time
from taobao_s.settings import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def data_cleaning(data):
    if ' ' in data:
        data = re.sub(' ', '', data)
    if "'" in data:
        data = re.sub("'", '', data)
    if r'\n' in data:
        data = re.sub(r'\\n', '', data)
    return data

def register():
    while True:
        browser = webdriver.FirefoxOptions()
        browser.add_argument('-headless')
        browser = webdriver.Firefox(firefox_options=browser)
        # browser = webdriver.Firefox()
        browser.get('https://login.taobao.com/member/login.jhtml')
        user = browser.find_element(By.ID, 'TPL_username_1')
        try:
            input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'forget-pwd.J_Quick2Static')))
            input.click()
        except Exception as e:
            print(e)
        user = browser.find_element(By.ID, 'TPL_username_1')
        password = browser.find_element(By.ID, 'TPL_password_1')
        user.send_keys(USER)
        time.sleep(random.random() * 2)
        password.send_keys(PASSWORD)
        time.sleep(random.random() * 1)
        browser.execute_script("Object.defineProperties(navigator,{webdriver:{get:() => false}})")
        action = ActionChains(browser)
        time.sleep(random.random() * 1)
        butt = browser.find_element(By.ID, 'nc_1_n1z')
        browser.switch_to.frame(browser.find_element(By.ID, '_oid_ifr_'))
        browser.switch_to.default_content()
        action.click_and_hold(butt).perform()
        action.reset_actions()
        action.move_by_offset(285, 0).perform()
        time.sleep(random.random() * 1)
        button = browser.find_element(By.ID, 'J_SubmitStatic')
        time.sleep(random.random() * 2)
        button.click()
        time.sleep(random.random() * 2)
        # browser.get('https://www.taobao.com/')
        cookie = browser.get_cookies()
        list = {}
        for cookiez in cookie:
            name = cookiez['name']
            value = cookiez['value']
            list[name] = value
        if len(list) > 10:
            break
        else:
            browser.close()
    return browser,list