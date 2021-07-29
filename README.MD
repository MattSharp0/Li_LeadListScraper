# Li(LinkedIn) Lead List Scraper

This program returns an excel document of linkedin profile links from a provided linkedin sales navigator lead list link.

run python app.py --help to learn more

#### Current bugs:

- Occasionally unable to locate lead location / account, offsetting lead name / links for entire list

#### Improvements to make:

- ~~Include lead name and title when scraping~~
- Include web driver install/setup instructions
- Improve readme formatting & documentation
- ~~Write list names in full~~
- Split lead name into first - last
- Improve CLI interface

**_Note:_** Requires linkedIn sales navigator account credentials and cannot be run if the account requires two-factor authentication. Provide credentials in dict CREDENTIALS in app.py
