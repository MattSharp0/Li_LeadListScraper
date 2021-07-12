from selenium.webdriver.chrome.options import Options
from scraper import ScraperDriver
from excel_writer import write_to_excel
# remove below import to run locally
from config import CREDENTIALS

# Uncomment and fill in to run
# CREDENTIALS = {'USERNAME': 'your username', 'PASSWORD': 'your password'}

lead_list_link = str(input('Paste lead list link here -> '))
path = input("\nSave directory (press enter to leave as default: Desktop): ")

# driver settings, comment out to run visibly
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
    list_of_profile_links = browser.get_profile_links()

    # If multiple pages exist; iterate and scrape
    if pages > 1:
        for page in page_links:
            browser.get(page)
            current_page_leads = browser.get_profile_links()
            for lead in current_page_leads:
                list_of_profile_links.append(lead)

    # check list validity and exit
    if len(list_of_profile_links) > 1:
        print(
            f'\nScrape complete!\n{len(list_of_profile_links)} links added to list')
        write_to_excel(list_of_profile_links, list_title, path.strip())
    else:
        print('\nError! List is empty')
        exit(1)
