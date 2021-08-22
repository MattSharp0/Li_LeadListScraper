# Li(LinkedIn) Lead List Scraper

A command line tool form scraping Linkedin sales navigator lead lists. Returns an excel doc with lead names, titles, accounts, locations and profile links.
With flag --as-csv will also return a csv file formatted for use with Zoominfo's Enhance feature.

To get started:

1. Clone repo into desired directory
2. Intall requirements
3. Install chromedriver - see [here](https://sites.google.com/chromium.org/driver/getting-started)
4. Enter Sales Nav credentials in app.py or in new file config.py

#### Current bugs:

-

#### Improvements to make:

- Include web driver install/setup instructions
- Improve readme formatting & documentation
- Setup as package
- Improve CLI interface
- ~~Write list names in full~~
- ~~Split lead name into first - last~~
- ~~Include lead name and title when scraping~~

**_Note:_** Requires linkedIn sales navigator account credentials and cannot be run if the account requires two-factor authentication. Provide credentials in dict CREDENTIALS in app.py or in config.py file
