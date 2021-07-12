This program returns an excel document of linkedin profile links from a provided linkedin sales navigator lead list link.

It is composed of three modules:

1. app.py: Takes list link and optional path to save file.

2. scraper.py: A Selenium Chrome driver extension, ScraperDriver (scraper.py). Supplies methods get_lead_list, get_list_data & get_profile_links

3. An xlsxwriter based Excel handler (excel_writer.py). Supplies method write_to_excel

Current bugs:

> Link has to be copied while on the lead list page in order for multi page support to function properly

Improvements still to make:

> Scrape lead name and title
> Take flag for running headless
> Check for and remove duplicates

Note: Requires linkedIn sales navigator account credentials and cannot be run if the account requires two-factor authentication. Provide credentials in dict CREDENTIALS in app.py
