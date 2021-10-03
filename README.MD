# Li (LinkedIn) Lead List Scraper

A command line tool for scraping Linkedin sales navigator lead lists. Returns an excel doc with lead names, titles, accounts, locations, notes and profile links.
With flag --as-csv will also return a csv file formatted for use with Zoominfo's Enhance feature.

To get started:

1. Clone repo into desired directory
2. Intall requirements `pipenv install -r requirements.txt`
3. Install chromedriver - see [here](https://sites.google.com/chromium.org/driver/getting-started)
4. Enter Sales Nav credentials and path to ChromeDriver in app.py or in a new file config.py

For best results ensure leads are connected to the correct account (LinkedIn frequently misaligns lead accounts / roles)

#### Current bugs:

-

#### Improvements to make:

- ~~Option to add domain for CSV files (works best when using with Zoominfo Enhance)~~
- ~~Improve CLI interface~~ - implemented [typer](https://github.com/tiangolo/typer)
- ~~Write list names in full~~
- ~~Split lead name into first - last~~
- ~~Include lead name and title when scraping~~

**_Note:_** Requires linkedIn sales navigator account credentials and cannot be run if your account requires multi-factor authentication.

**_Disclaimer:_** Use of this software may infringe upon [LinkedIn's user agreement](<https://www.linkedin.com/legal/user-agreement#:~:text=Develop%2C%20support%20or%20use%20software%2C%20devices%2C%20scripts%2C%20robots%20or%20any%20other%20means%20or%20processes%20(including%20crawlers%2C%20browser%20plugins%20and%20add-ons%20or%20any%20other%20technology)%20to%20scrape%20the%20Services%20or%20otherwise%20copy%20profiles%20and%20other%20data%20from%20the%20Services%3B>). Use at your own risk.
