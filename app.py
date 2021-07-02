from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from openpyxl import Workbook
from config import username, password

lead_list_name = input('Type lead list name: ')


def scrape_lead_list(lead_list_name):
    # set options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')

    # create driver object
    with webdriver.Chrome(options=options) as browser:
        # load sales navigator
        browser.get('https://www.linkedin.com/sales')

        # sign in
        username_box = browser.find_element_by_id('username')
        username_box.send_keys(username)
        password_box = browser.find_element_by_id('password')
        password_box.send_keys(password)
        try:
            signin_button = browser.find_element_by_xpath(
                '//*[@id="app__container"]/main/div[2]/form/div[3]/button')
            signin_button.click()
            print('\nSigned in, loading hompage...')
        except NoSuchElementException():
            exit(1)

        # Wait for homepage to load, then go to Lead lists
        WebDriverWait(browser, 10).until(
            lambda b: b.find_element_by_id('ember14'))
        try:
            lead_lists = browser.find_element_by_id('ember14')
            lead_lists.click()
            print('\nLoading lead lists page...')
        except NoSuchElementException():
            exit(1)

        # Wait for Lead lists to load, then go to specified list
        WebDriverWait(browser, 10).until(lambda b: b.find_element_by_xpath(
            f"//*[text()='{lead_list_name}']//ancestor::a"))
        try:
            lead_list = browser.find_element_by_xpath(
                f"//*[text()='{lead_list_name}']//ancestor::a")
            lead_list.click()
            print('\nLoading target lead list...')
        except NoSuchElementException():
            exit(1)

        # wait for target Lead List to load, then add <a> elements to list
        WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
            'lists-detail__view-profile-name-link'))
        try:
            leads = browser.find_elements_by_class_name(
                'lists-detail__view-profile-name-link')
            print(f'\nSaving {len(leads)} lead elements to list...')
        except NoSuchElementException():
            exit(1)

        # Get url (href) from a tag and add to list
        list_of_lead_links = [lead.get_attribute('href') for lead in leads]

        # check list validity and exit
        if len(list_of_lead_links) > 1:
            print('\nList of lead links created')
            return list_of_lead_links
        else:
            print('\nError: empty list')
            exit(1)


def write_to_excel(link_list, lead_list_name):
    if len(link_list) < 1:
        print('\nList empty!')
        exit(1)

    print('\nWriting list to excel...')
    title = ((lead_list_name.split()[0]) + ' leads')
    wb = Workbook()
    sheet = wb.create_sheet('lead list', 0)
    sheet['A1'].value = title

    r = 2
    for link in link_list:
        box = sheet.cell(r, 1)
        box.value = link
        r += 1

    wb.save(f'{title}.xlsx')

    print(f'\nSaved {len(link_list)} lead links to {title}.xlsx')


leads = (scrape_lead_list(lead_list_name))
# print(leads)

write_to_excel(leads, lead_list_name)
