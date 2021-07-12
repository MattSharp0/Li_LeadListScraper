from selenium.webdriver.chrome.options import Options
from scraper import ScraperDriver
from xlsx_writer import write_to_excel
from config import CREDENTIALS

'''
Current bugs:
/

Improvements to make: 
>Save Excel doc to specific path
>Scrape lead name and title
>Check for and remove duplicates
>Take flag for running headless
'''

lead_list_link = str(input('Past lead list link here -> '))

options = Options()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')

# create driver object
with ScraperDriver(options=options) as browser:

    # Create webdriver object, load sales nav, sign in and go to list
    browser.get_lead_list(CREDENTIALS, lead_list_link.strip())

    # Get list title, pages and create page links
    list_title, current_page, pages, page_links = browser.get_list_data()

    # Scape leads of first page
    list_of_profile_links = browser.scrape_leads()

    # If multiple pages exist; iterate and scrape
    if pages > 1:
        for page in page_links:
            browser.get(page)
            current_page_leads = browser.scrape_leads()
            for lead in current_page_leads:
                list_of_profile_links.append(lead)

    # check list validity and exit
    if len(list_of_profile_links) > 1:
        print(
            f'\nScrape complete!\n{len(list_of_profile_links)} links added to list')
        write_to_excel(list_of_profile_links, list_title,)
    else:
        print('\nError! List is empty')
        exit(1)
