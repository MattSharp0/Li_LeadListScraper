
import os
from src.wsdriver import WebScraperDriver, options
from src.file_writer import write_to_excel, write_to_csv
import typer
# Remove below to run locally
from config import CREDENTIALS, CHROMEDRIVER_PATH


def main(as_xlsx: bool = True, as_csv: bool = False):
    '''
    Scrape lead list from provided link(s) and returns an Excel doc and / or a CSV file. 
    Optionally specify whether to save as .xlsx file, default is True. 
    Optionally specify whether to save as .CSV file, default is False.
    '''

    lead_list_links = typer.prompt('\n- Paste lead lists seperated by comma')

    lead_lists = lead_list_links.split(',')
    total_lists = len(lead_lists)

    start = typer.confirm(
        f'\n- Provided {total_lists} list link(s)\n- Begin scrape?', abort=True)

    # Supply credentials & path to chromedriver below:
    # CREDENTIALS = {'USERNAME' : 'your_username_here', 'PASSWORD': 'your_password_here'}
    # CHROMEDRIVER_PATH = 'your_chromedriver_path_here'

    # set save path
    path = os.path.expanduser('~/Desktop/leads')
    if not os.path.isdir(path):
        os.mkdir(path)

    BAD_CHARS = '!@#$%^&*{}[]+=\\|/.,><~`\'\":;'

    # create Scraper Driver object
    if start:
        with WebScraperDriver(options=options, executable_path=CHROMEDRIVER_PATH) as driver:
            typer.secho('\n- Created chromedriver object')

            # Sign in with provided credentials
            driver.sign_in(credentials=CREDENTIALS)
            typer.secho('\n- Signed into LinkedIn Sales Nav')

            total_leads = 0
            typer.secho('\n- Scraping lists...')

            # Iterate through lists, scape and save
            with typer.progressbar(lead_lists, label='Scraping lists') as progress:
                for lead_list in progress:
                    lead_list_formated = (lead_list.strip()).split(
                        '?')[0] + '?sortCriteria=NAME&sortOrder=ASCENDING'

                    # Go to list and scrape leads
                    list_title, lead_data, number_of_leads = driver.scrape_lead_list(
                        lead_list_link=lead_list_formated)

                    total_leads += number_of_leads

                    # Remove list title notes. ex: list title [some note I wrote] -> list title
                    file_name = (list_title.split('[')[0]).strip()

                    # Removes error causing characters
                    for char in BAD_CHARS:
                        file_name = file_name.replace(char, '')

                    if as_xlsx:
                        # Write leads to excel document
                        write_to_excel(data_list=lead_data,
                                       file_name=file_name, path=path)
                    if as_csv:
                        # Write leads to CSV
                        domain = typer.prompt(
                            text=f'\nFor best result with Zoominfo Enhance, please provide the company domain for leads in list \'{list_title}\' \n(ex. for a list of google employees use google.com) \nLeave blank to use company name instead', default='')
                        write_to_csv(data_list=lead_data, domain=domain,
                                     file_name=file_name, path=path)

                    typer.secho(
                        f'\n- Saved {number_of_leads} leads from {list_title}')

    else:
        typer.secho('- Canceling scrape')

    typer.secho(
        f'\n- Completed scrape \n- Saved {total_leads} leads from {total_lists} lists')


#  Run using Typer for CLI args/options
if __name__ == "__main__":
    typer.run(main)
