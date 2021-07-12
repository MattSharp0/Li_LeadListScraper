from selenium.webdriver.chrome.options import Options
from scraper import ScraperDriver
from xlsx_writer import write_to_excel
from config import CREDENTIALS

'''
Current bugs:
>Not scraping second page links (adds 1st page links again)
>ElementClickInterceptedException when clicking next page after 2nd page
>Inconsistent detection of multipule pages (detecting incorrect amount)

Improvements to make: 
>Find by link instead of list name
    >Signin
    >Load homepage
    >Go to list link
    >Get list title
    >Scrape and write to excel
>Save Excel doc to specific path
>Scrape lead name and title
>Check for and remove duplicates
>Take flag for running headless
'''

lead_list_name = str(input('Type lead list name: '))

options = Options()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')

# create driver object
with ScraperDriver(options=options) as browser:
    # Load linkedin sales nav, sign in and find list
    browser.go_to_lead_list(CREDENTIALS, lead_list_name)

    # Get number of pages and links
    current_page, pages, page_links = browser.get_list_pages()

    # Scape leads of first page
    list_of_lead_links = browser.scrape_leads()

    # Iterate through pages, scrape leads and append to list
    if pages > 1:
        for page in page_links:
            browser.get(page)
            current_page_leads = browser.scrape_leads()
            for lead in current_page_leads:
                list_of_lead_links.append(lead)

    # check list validity and exit
    if len(list_of_lead_links) > 1:
        print(
            f'\nScrape complete!\n{len(list_of_lead_links)} links added to list')
        write_to_excel(list_of_lead_links, lead_list_name,)
    else:
        print('\nError! List is empty')
        exit(1)
