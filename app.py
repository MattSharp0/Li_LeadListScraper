from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from openpyxl import Workbook
from config import USERNAME, PASSWORD

# lead_list_name = input('Type lead list name: ')

# test lists:
# lead_list_name = 'bb&t (now truist) [jc] [submitted]'
lead_list_name = 'Ambassador [MH] [submitted]'

'''
Commented out write to excel funtion call
Set scrape to no longer run headless
'''


def scrape_lead_list(lead_list_name):
    '''
    Scrapes LinkedIn profile links from provided sales navigator lead list and returns them as a list.

    :Args:
    list: lead_list_name

    :Returns:
    list of lead links

    Note:
    Requires sales navigator credentials imported as USERNAME and PASSWORD
    '''

    # set webdriver options
    options = Options()

    # options.add_argument('--headless')
    # options.add_argument('window-size=1920x1080')

    # create driver object
    with webdriver.Chrome(options=options) as browser:
        # load sales navigator
        browser.get('https://www.linkedin.com/sales')
        print('\n  Chrome driver object created\n    Signing into LinkedIn Sales Nav...')

        # Sign in
        try:
            username_box = browser.find_element_by_id('username')
            username_box.send_keys(USERNAME)
            password_box = browser.find_element_by_id('password')
            password_box.send_keys(PASSWORD)

            signin_button = browser.find_element_by_xpath(
                '//*[@id="app__container"]/main/div[2]/form/div[3]/button')
            signin_button.click()
            print('\n  Signed in!\n    Loading homepage...')
        except NoSuchElementException as e:
            print(e)
            exit()
        except StaleElementReferenceException as e:
            print(e)
            exit()

        # Wait for homepage to load, then go to Lead lists
        try:
            WebDriverWait(browser, 10).until(
                lambda b: b.find_element_by_id('ember14'))
            print('\n  Homepage loaded!')

            lead_lists = browser.find_element_by_id('ember14')
            lead_lists.click()
            print('    Loading lead lists page...')
        except TimeoutException as e:
            print(e)
            exit(1)
        except StaleElementReferenceException as e:
            print(e)
            exit(1)
        except NoSuchElementException as e:
            print(e)
            exit(1)

        # Wait for Lead lists to load
        try:
            WebDriverWait(browser, 10).until(lambda b: b.find_element_by_xpath(
                f"//*[text()='{lead_list_name}']//ancestor::a"))
            print('\n  Lead lists page loaded!')
        except TimeoutException as e:
            print(e)
            exit()

        # Go to target lead list
        try:
            browser.find_element_by_xpath(
                f"//*[text()='{lead_list_name}']//ancestor::a").click()
            print(f'    Loading target lead list: {lead_list_name}...')
        except StaleElementReferenceException as e:
            print(
                f'\nError: Lead list: "{lead_list_name}" is no longer visible\n')
            print(e)
            exit()
        except NoSuchElementException as e:
            print(f'Error: Could not find list: "{lead_list_name}"')
            print(e)
            exit()

        def create_list_of_links(page_loaded=False):
            '''
            Finds and adds profile links to list

            :Args:
            page_loaded: Optional bolean parameter

            :Returns:
            current_page_links - a list of profile links from page
            '''
            if not page_loaded:
                WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
                    'lists-detail__view-profile-name-link'))
                print('\n  Target lead list page loaded!')

            print('    Scraping lead profile links...')
            profile_links = browser.find_elements_by_class_name(
                'lists-detail__view-profile-name-link')

            current_page_links = [profile_link.get_attribute(
                'href') for profile_link in profile_links]

            print(f'\n  Saved {len(profile_links)} links from page to list!')
            return current_page_links

        # Handle multiple pages:

        def get_current_page_number():
            # Wait for page numbers to load
            WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
                'artdeco-pagination__indicator--number'))

            # Find current page number
            current_page = browser.find_element_by_xpath(
                '//*[@class="artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view"]/button/span[1]')
            current_page_number = current_page.text
            return int(current_page_number)

        # Get current page:
        current_page = get_current_page_number()
        print(f'\n  On page {current_page}')

        # Get number of pages
        WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
            'artdeco-pagination__indicator'))

        pages = len(browser.find_elements_by_class_name(
            'artdeco-pagination__indicator'))
        print(f'\n    Found {pages} pages...')

        # Main list of links to be returned
        list_of_lead_links = create_list_of_links(page_loaded=False)

        # While multiple pages exist, go page by page and copy lead links to list
        while current_page < pages:
            # Find and click next page button
            WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
                'artdeco-pagination__button--next'))

            next_page = browser.find_element_by_class_name(
                'artdeco-pagination__button--next')
            next_page.click()

            # Update current page number
            current_page = get_current_page_number()
            print(f'\n    Loading page {current_page}/{pages}...')

            # For debugging:
            list_of_lead_links.append(current_page)

            # Add links to main list
            for link in create_list_of_links(page_loaded=False):
                list_of_lead_links.append(link)

        # check list validity and exit
        total_leads = len(list_of_lead_links)
        if total_leads > 1:
            print(f'\nScrape complete!\n{total_leads} links added to list')
            return list_of_lead_links
        else:
            print('\nError! List is empty')
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
print(leads)

# write_to_excel(leads, lead_list_name)
