from os import link
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, WebDriverException

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920x1080')


class WebScraperDriver(webdriver.Chrome):
    '''
    Extends webdriver class with specifc methods for navigating linkedin sales navigator
    '''

    def sign_in(self, credentials):
        '''
        Load and login to linkedin sales navigator

        :Params:
        credentials: dict: LinkedIn sales nav login and password

        :Returns:
        boolean requires_code: true if login code is required 
        '''
        username, password = credentials['USERNAME'], credentials['PASSWORD']

        # load sales navigator
        self.get('https://www.linkedin.com/sales')

        WebDriverWait(self, 10).until(
            lambda b: b.find_element_by_id('username'))
        # Sign in
        username_box = self.find_element_by_id('username')
        username_box.send_keys(username)
        password_box = self.find_element_by_id('password')
        password_box.send_keys(password)

        signin_button = self.find_element_by_xpath(
            '//*[@id="app__container"]/main/div[2]/form/div[3]/button')
        signin_button.click()
        try:
            # Wait for homepage to load, then go to Lead lists
            WebDriverWait(self, 10).until(
                lambda b: b.find_element_by_id('ember9'))

        except WebDriverException:
            print('\n- Error: Homepage failed to load')

    def get_list_data(self):
        '''
        Finds lead list title, total number of pages and creates links to each page

        :Returns:
        Str: Lead list title
        int: number of pages
        list: page urls
        '''

        # Wait for list title to load and save it
        WebDriverWait(self, 10).until(
            lambda b: b.find_elements_by_class_name('lists-nav__list-name'))
        title_element = self.find_element_by_class_name('lists-nav__list-name')
        title = title_element.text

        # Wait for page numbers to load
        WebDriverWait(self, 10).until(lambda b: b.find_elements_by_class_name(
            'artdeco-pagination__indicator--number'))

        # Find total pages
        pages = len(self.find_elements_by_class_name(
            'artdeco-pagination__indicator--number'))

        # Create page links for each page of list
        current_page_link = self.current_url
        page_split = str(current_page_link).split('?')
        page_urls = []

        for page in range(2, (pages+1)):
            page_url = f'?page={page}&'.join(page_split)
            page_urls.append(page_url)

        return title, pages, page_urls

    def get_profile_links(self):
        '''
        Finds and adds profile links to list

        :Returns:
        list: current_page_links: a list of profile links from page
        '''
        # Wait for lead list to load
        WebDriverWait(self, 10).until(lambda b: b.find_elements_by_class_name(
            'lists-detail__view-profile-name-link'))
        print('\n- Target lead list page loaded!')

        # Collect profile elements
        print('- Scraping lead profile links...')
        profile_links = self.find_elements_by_class_name(
            'lists-detail__view-profile-name-link')

        # Get profile linkss
        current_page_links = [profile_link.get_attribute(
            'href') for profile_link in profile_links]

        print(f'\n- Saved {len(profile_links)} links from page to list!')
        return current_page_links

    def get_lead_data(self):
        '''
        Scrapes lead data (Name, title, account, location, profile link) from page

        :returns: 
        list: list of lead data lists
        int: total leads found
        '''
        WebDriverWait(self, 10).until(lambda b: b.find_elements_by_class_name(
            'lists-detail__view-profile-name-link'))

        lead_data = []

        table = self.find_element_by_tag_name('tbody')
        table_rows = table.find_elements_by_tag_name('tr')

        for row in table_rows:
            lead = row.find_element_by_class_name(
                'lists-detail__view-profile-name-link')
            name = (lead.text).title()

            profile_link = lead.get_attribute('href')

            try:
                lead_title_element = row.find_element_by_xpath(
                    './td[1]/div/div[2]/div[2]/span/div')
                title = lead_title_element.text
            except NoSuchElementException:
                title = ''

            try:
                lead_account_element = row.find_element_by_class_name(
                    'artdeco-entity-lockup__title--alt-link')
                account = lead_account_element.text
            except NoSuchElementException:
                account = ''

            try:
                lead_location_element = row.find_element_by_class_name(
                    'list-people-detail-header__geography')
                location = lead_location_element.text
            except NoSuchElementException:
                location = ''

            lead_data.append([name, title, account, location, profile_link])

        return lead_data, len(table_rows)

    def scrape_lead_list(self, lead_list_link):
        '''
        Scrapes data from lead list

        :params:
        lead_list_link: url of lead list

        :returns:
        title: str of page title
        list_of_profile_links: list of all profile links from lead list
        '''

        self.get(lead_list_link)

        title, pages, page_links = self.get_list_data()

        # Scape leads of first page
        lead_data, total_leads = self.get_lead_data()

        # If multiple pages exist; load and scrape
        if pages > 1:
            for page in page_links:
                self.get(page)
                page_lead_data, leads_on_page = self.get_lead_data()
                total_leads += leads_on_page
                for lead in page_lead_data:
                    lead_data.append(lead)

        return title, lead_data, total_leads
