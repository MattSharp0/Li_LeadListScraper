from os import path
from posixpath import split
from src.wsdriver import WebScraperDriver, options
from src.excel_writer import write_to_excel
import typer
# Remove below to run locally
from config import CREDENTIALS


def main(save_path: str = ''):
    '''
    Scrape lead list from provided link(s) and returns an excel documment. 
    Requires lead link (str) (seperate multiple with ',')
    Optionally specify directory path to save file (defaults to desktop)
    '''

    lead_list_links = typer.prompt('\n- Paste lead lists seperated by comma')

    lead_lists = lead_list_links.split(',')
    total_lists = len(lead_lists)

    start = typer.confirm(
        f'\n- Provided {total_lists} list link(s)\n- Begin scrape?', abort=True)

    # Supply credentials below:
    # CREDENTIALS = {'USERNAME' : 'your_username', 'PASSWORD': 'your_password'}

    # create Scraper Driver object
    if start:
        with WebScraperDriver(options=options) as driver:
            typer.secho('\n- Created chromedriver object')
            # Sign in with provided credentials
            driver.sign_in(credentials=CREDENTIALS)
            typer.secho('\n- Signed into LinkedIn Sales Nav')

            total_leads = 0
            typer.secho('\n- Scraping lists...')
            with typer.progressbar(lead_lists, label='Scraping lists') as progress:
                for lead_list in progress:
                    lead_list_formated = (lead_list.strip()).split(
                        '?')[0] + '?sortCriteria=NAME&sortOrder=ASCENDING'
                    # Go to list and scrape leads
                    title, lead_data, list_leads = driver.scrape_lead_list(
                        lead_list_link=lead_list_formated)
                    total_leads += list_leads
                    # Write leads to excel document
                    write_to_excel(data_list=lead_data,
                                   list_title=title, path=save_path)
                    typer.secho(
                        f'\n- Saved {list_leads} leads from {title}')

    else:
        typer.secho('- Canceling scrape')

    typer.secho(
        f'\n- Completed scrape \n- Saved {total_leads} leads from {total_lists} lists')


#  Run using Typer for CLI args/options
if __name__ == "__main__":
    typer.run(main)
