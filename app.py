from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from scraper import ScraperDriver
from xlsx_writer import write_to_excel
from config import CREDENTIALS

'''
Current bugs:
>Not scraping second page links (adds 1st page links again)
>ElementClickInterceptedException when clicking next page after 2nd page
>Inconsistent detection of multipule pages (detecting incorrect amount)

Improvements to make: 
>Save Excel doc to specific path
>Scrape lead name and title
>Check for and remove duplicates
>Take flag for running headless
'''

lead_list_name = str(input('Type lead list name: '))

# test lists:
# lead_list_name = 'CaptialOne [mh]'

options = Options()
# options.add_argument('--headless')
# options.add_argument('window-size=1920x1080')

# create driver object
with ScraperDriver(options=options) as browser:
    browser.go_to_lead_list(CREDENTIALS, lead_list_name)

    list_of_lead_links = browser.scrape_leads()

    current_page, pages = browser.get_page_numbers()

    # While multiple pages exist, go page by page and copy lead links to list
    while current_page < pages:
        # Find and click next page button
        try:
            WebDriverWait(browser, 10).until(lambda b: b.find_elements_by_class_name(
                'artdeco-pagination__button--next'))

            next_page = browser.find_element_by_class_name(
                'artdeco-pagination__button--next')
            next_page.click()
            print('\n    Loading next page...')
        except ElementClickInterceptedException as e:
            print(e)
            exit(1)

        # Update current page number
        current_page, pages = browser.get_page_numbers()

        # For debugging:
        list_of_lead_links.append(f'{current_page}/{pages}')

        # Add links to main list
        browser.implicitly_wait(5)

        current_page_links = browser.create_list_of_links()

        for link in current_page_links:
            list_of_lead_links.append(link)

    # check list validity and exit
    if len(list_of_lead_links) > 1:
        print(
            f'\nScrape complete!\n{len(list_of_lead_links)} links added to list')
        write_to_excel(list_of_lead_links, lead_list_name,)
    else:
        print('\nError! List is empty')
        exit(1)
