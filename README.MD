# Li (LinkedIn) Lead List Scraper

A command line tool for scraping Linkedin sales navigator lead lists. Returns an excel doc with lead names, titles, accounts, locations, notes and profile links.
With flag --as-csv will also return a csv file formatted for use with Zoominfo's Enhance feature.

To get started:

1. Clone repo into desired directory
2. Intall requirements
3. Install chromedriver - see [here](https://sites.google.com/chromium.org/driver/getting-started)
4. Enter Sales Nav credentials in app.py or in new file config.py

For best results ensure leads are connected to the correct account (LinkedIn frequently misaligns lead accounts / roles)

#### Current bugs:

- wip: Zoominfo Enhance works best with `first_name, last_name, company_domain` format. Working on it!

#### Improvements to make:

- Improve CLI interface
- ~~Write list names in full~~
- ~~Split lead name into first - last~~
- ~~Include lead name and title when scraping~~

**_Note:_** Requires linkedIn sales navigator account credentials and cannot be run if the account requires two-factor authentication. Provide credentials in dict CREDENTIALS in app.py or in config.py file.
