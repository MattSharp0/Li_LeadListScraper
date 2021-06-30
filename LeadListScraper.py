import time
from selenium import webdriver
from openpyxl import Workbook
from config import username, password

list_name = 'NMI [jc]'

with webdriver.Chrome() as browser:
    browser.get('https://www.linkedin.com/sales')

    try:
        username_box = browser.find_element_by_id('username')
        username_box.send_keys(username)

        password_box = browser.find_element_by_id('password')
        password_box.send_keys(password)

        browser.find_element_by_xpath(
            '//*[@id="app__container"]/main/div[2]/form/div[3]/button').click()
    except:
        print('Sign in failed')

    try:
        time.sleep(3)
        browser.find_element_by_id('ember14').click()

        time.sleep(3)
        browser.find_element_by_xpath(
            f"//*[text()='{list_name}']//ancestor::a").click()
    except:
        print('unable to locate lead list')

    time.sleep(3)
    leads = browser.find_elements_by_class_name(
        'lists-detail__view-profile-name-link')
    lead_links = [lead.get_attribute('href') for lead in leads]
