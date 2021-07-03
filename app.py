from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from openpyxl import Workbook
from config import USERNAME, PASSWORD

lead_list_name = input('Type lead list name: ')

'''
Commented out write to excel funtion call
Set scrape to no longer run headless
'''


def scrape_lead_list(lead_list_name):
    '''
    Scrapes LinkedIn profile links from provided sales navigator lead list and returns them as a list.

    Requires String Arg: lead_list_name

    Requires sales navigator credentials imported as USERNAME and PASSWORD
    '''

    # set webdriver options
    options = Options()

    # UNCOMMENT BELOW OPTIONS
    # options.add_argument('--headless')
    # options.add_argument('window-size=1920x1080')

    # create driver object
    with webdriver.Chrome(options=options) as browser:
        # load sales navigator
        browser.get('https://www.linkedin.com/sales')

        # sign in
        username_box = browser.find_element_by_id('username')
        username_box.send_keys(USERNAME)
        password_box = browser.find_element_by_id('password')
        password_box.send_keys(PASSWORD)

        signin_button = browser.find_element_by_xpath(
            '//*[@id="app__container"]/main/div[2]/form/div[3]/button')
        signin_button.click()
        print('\nSigned in, loading hompage...')

        # Wait for homepage to load, then go to Lead lists
        try:
            WebDriverWait(browser, 10).until(
                lambda b: b.find_element_by_id('ember14'))
        except TimeoutException():
            print(
                '\nTimed out loading homepage; could not find "Lead Lists" element (id=ember14)')
            exit(1)

        lead_lists = browser.find_element_by_id('ember14')
        lead_lists.click()
        print('\nLoading lead lists page...')

        # Wait for Lead lists to load, then go to specified list
        try:
            WebDriverWait(browser, 10).until(lambda b: b.find_element_by_xpath(
                f"//*[text()='{lead_list_name}']//ancestor::a"))
        except TimeoutException():
            print(f'\nTimed out loading "{lead_list_name}" element')
            exit(1)
        except NoSuchElementException():
            print(
                f'\nCould not find "{lead_list_name}" on page')
            exit(1)

        lead_list = browser.find_element_by_xpath(
            f"//*[text()='{lead_list_name}']//ancestor::a")
        lead_list.click()
        print('\nLoading target lead list...')

        # Wait for target Lead List to load
        try:
            WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
                'lists-detail__view-profile-name-link'))
        except TimeoutException():
            print('\nTimed out loading lead list')
            exit(1)

        def create_list_of_links(loaded=False):
            '''
            Finds and adds profile links to list

            Takes optional bolean parameter loaded

            Returns current_page_links
            '''
            if not loaded:
                WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
                    'lists-detail__view-profile-name-link'))

            profile_links = browser.find_elements_by_class_name(
                'lists-detail__view-profile-name-link')
            print(f'\nSaving {len(profile_links)} lead elements to list...')

            current_page_links = [profile_link.get_attribute(
                'href') for profile_link in profile_links]

            return current_page_links

        list_of_lead_links = create_list_of_links(loaded=True)

        # Create list of pages
        pages = browser.find_elements_by_class_name(
            'artdeco-pagination__indicator--number')
        current_page = browser.find_element_by_xpath(
            '//*[@class="artdeco-pagination__indicator--number active selected"]/button/span[1]')
        current_page_number = current_page.text

        if len(pages) > 1:
            # got to next page and find links, repeat until next button no longer visible
            pass

        # # Add <a> tag href attribute to list
        # profile_links = browser.find_elements_by_class_name(
        #     'lists-detail__view-profile-name-link')
        # print(f'\nSaving {len(profile_links)} lead elements to list...')

        # list_of_lead_links = [profile_link.get_attribute(
        #     'href') for profile_link in profile_links]

        # check list validity and exit
        if len(list_of_lead_links) > 1:
            print('\nList of lead links created!')
            return list_of_lead_links
        else:
            print('\nError: empty list')
            exit(1)


def write_to_excel(link_list, lead_list_name):
    '''
    Takes a list of links and writes them to an excel document with the list name as the title

    Requires list of strings/ints

    Requires list name
    '''

    # Quit if list has no items
    if len(link_list) < 1:
        print('\nList empty!')
        exit(1)

    # Create document and sheet
    print('\nWriting list to excel...')
    wb = Workbook()
    sheet = wb.create_sheet('lead list', 0)

    # Format title
    title = ((lead_list_name.split()[0]) + ' leads')

    # Write title
    sheet['A1'].value = title

    # Write links to A column
    r = 2
    for link in link_list:
        box = sheet.cell(r, 1)
        box.value = link
        r += 1

    # Save document with title
    wb.save(f'{title}.xlsx')

    print(f'\nSaved {len(link_list)} lead links to {title}.xlsx')


leads = (scrape_lead_list(lead_list_name))
# print(leads)

# write_to_excel(leads, lead_list_name)
