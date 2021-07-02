This program (app.py) returns an excel document of linkedin profile links from a proivded linkedin sales navigator lead list.

It is composed of two parts:

1. A selenium (requires Chrome driver) based scraper function (scrape_lead_list(lead_list_name)) which takes as a paremter the lead list name and returns a list of linkedin profile links

2. An OpenPyXl based Excel doc creator (write_to_excel(link_list, lead_list_name)) which takes the parameters a list of links and the lead list name and creates an excel document in the local directory.


Note: Requires linkedIn sales navigator account credentials and cannot be run if the account requires two-factor authentication. Credentials are supplied in config.py as USERNAME and PASSWORD.
