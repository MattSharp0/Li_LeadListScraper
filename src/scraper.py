
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class ScraperDriver(webdriver.Chrome):
    '''
    Extends webdriver class with specifc methods for navigating linkedin sales navigator
    '''

    def get_lead_list(self, credentials, lead_list_link):
        '''
        Navigates to Sales Nav lead list and returns drier object on page

        :Params:
        credentials: dict: LinkedIn sales nav login and password
        lead_list_link: str: lead list title

        :Returns:
        Chrome webdriver on lead list page
        '''

        USERNAME, PASSWORD = credentials['USERNAME'], credentials['PASSWORD']

        # load sales navigator
        self.get('https://www.linkedin.com/sales')
        print('\n  Chrome driver object created\n    Signing into LinkedIn Sales Nav...')

        # Sign in
        try:
            username_box = self.find_element_by_id('username')
            username_box.send_keys(USERNAME)
            password_box = self.find_element_by_id('password')
            password_box.send_keys(PASSWORD)

            signin_button = self.find_element_by_xpath(
                '//*[@id="app__container"]/main/div[2]/form/div[3]/button')
            signin_button.click()
            print('\n  Signed in!\n    Loading homepage...')
        except NoSuchElementException as e:
            print(e)
            exit()

        # Wait for homepage to load, then go to Lead lists
        try:
            WebDriverWait(self, 10).until(
                lambda b: b.find_element_by_id('ember9'))
            print('\n  Homepage loaded!')
        except TimeoutException as e:
            print(e)
            exit()

        self.get(lead_list_link)
        print('    Loading lead list...')

        return self

    def get_list_data(self):
        '''
        Finds lead list title, current page number, total number of pages and creates links to each page

        :Returns:
        Str: Lead list title
        int: current page number
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

        # Find current page number
        current_page = self.find_element_by_xpath(
            '//*[@class="artdeco-pagination__indicator artdeco-pagination__indicator--number active selected ember-view"]/button/span[1]')
        current_page_number = current_page.text

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

        return title, int(current_page_number), pages, page_urls

    def get_profile_links(self):
        '''
        Finds and adds profile links to list

        :Returns:
        list: current_page_links: a list of profile links from page
        '''
        # Wait for lead list to load
        WebDriverWait(self, 10).until(lambda b: b.find_elements_by_class_name(
            'lists-detail__view-profile-name-link'))
        print('\n  Target lead list page loaded!')

        # Collect profile elements
        print('    Scraping lead profile links...')
        profile_links = self.find_elements_by_class_name(
            'lists-detail__view-profile-name-link')

        # Get profile linkss
        current_page_links = [profile_link.get_attribute(
            'href') for profile_link in profile_links]

        print(f'\n  Saved {len(profile_links)} links from page to list!')
        return current_page_links
