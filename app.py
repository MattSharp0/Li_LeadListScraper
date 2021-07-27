from posixpath import split
from src.wsdriver import WebScraperDriver, options
from src.excel_writer import write_to_excel
import typer
# Remove below to run locally
from config import CREDENTIALS


def main(lead_list_links: str, save_path: str = ''):
    '''
    Scrape lead list from provided link(s) and returns an excel documment. 
    Requires lead link (str) (seperate multiple with ',')
    Optionally specify directory path to save file (defaults to desktop)
    '''

    lead_lists = lead_list_links.split(',')
    total_lists = len(lead_lists)

    start = input(
        f'- Provided {total_lists} list link(s)\n- Begin scrape? Y/n ')

    # Supply credentials below:
    # CREDENTIALS = {'USERNAME' : 'your_username', 'PASSWORD': 'your_password'}

    # create Scraper Driver object
    if start.lower() == 'y':
        with WebScraperDriver(options=options) as driver:

            # Sign in with provided credentials
            driver.sign_in(credentials=CREDENTIALS)

            for lead_list in lead_lists:
                lead_list_formated = (lead_list.strip()).split(
                    '?')[0] + '?sortCriteria=NAME&sortOrder=ASCENDING'
                # Go to list and scrape leads
                title, list_of_profile_links = driver.scrape_lead_list(
                    lead_list_link=lead_list_formated)

                # Write leads to excel document
                write_to_excel(link_list=list_of_profile_links,
                               list_title=title, path=save_path)

    else:
        print('- Canceling scrape')

    print(f'\n- Completed scrape; saved {total_lists} lists\n')


#  Run using Typer for CLI args/options
if __name__ == "__main__":
    typer.run(main)
