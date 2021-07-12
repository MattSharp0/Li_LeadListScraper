
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException


class ScraperDriver(webdriver.Chrome):
    '''
    Extends webdriver class with leadlist specifc methods
    '''

    def go_to_lead_list(self, credentials, lead_list_name):
        '''
        Navigates to Sales Nav lead list and returns drier object on page

        :Params:
        credentials: dict: LinkedIn sales nav login and password
        lead_list_name: str: lead list title

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
        except StaleElementReferenceException as e:
            print(e)
            exit()

        # Wait for homepage to load, then go to Lead lists
        try:
            WebDriverWait(self, 10).until(
                lambda b: b.find_element_by_id('ember14'))
            print('\n  Homepage loaded!')

            lead_lists = self.find_element_by_id('ember14')
            lead_lists.click()
            print('    Loading lead lists page...')
        except TimeoutException as e:
            print(e)
            exit(1)
        except StaleElementReferenceException as e:
            print(e)
            exit(1)
        except NoSuchElementException as e:
            print(e)
            exit(1)

        # Wait for Lead lists to load
        try:
            WebDriverWait(self, 10).until(lambda b: b.find_element_by_xpath(
                f"//*[text()='{lead_list_name}']//ancestor::a"))
            print('\n  Lead lists page loaded!')
        except TimeoutException as e:
            print(e)
            exit()

        # Go to target lead list
        try:
            self.find_element_by_xpath(
                f"//*[text()='{lead_list_name}']//ancestor::a").click()
            print(f'    Loading target lead list: {lead_list_name}...')
        except StaleElementReferenceException as e:
            print(
                f'\nError: Lead list: "{lead_list_name}" is no longer visible\n')
            print(e)
            exit()
        except NoSuchElementException as e:
            print(f'Error: Could not find list: "{lead_list_name}"')
            print(e)
            exit()

        return self

    def get_list_pages(self):
        '''
        Finds current lead list page number and total number of pages

        :Returns:
        int: current page number
        int: number of pages
        list: page urls
        '''
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

        current_page_link = self.current_url
        page_split = str(current_page_link).split('?')
        page_urls = []

        for page in range(2, (pages+1)):
            page_url = f'?page={page}&'.join(page_split)
            page_urls.append(page_url)

        return int(current_page_number), pages, page_urls

    def scrape_leads(self):
        '''
        Finds and adds profile links to list

        :Returns:
        list: current_page_links: a list of profile links from page
        '''

        WebDriverWait(self, 10).until(lambda b: b.find_elements_by_class_name(
            'lists-detail__view-profile-name-link'))
        print('\n  Target lead list page loaded!')

        print('    Scraping lead profile links...')
        profile_links = self.find_elements_by_class_name(
            'lists-detail__view-profile-name-link')

        current_page_links = [profile_link.get_attribute(
            'href') for profile_link in profile_links]

        print(f'\n  Saved {len(profile_links)} links from page to list!')
        return current_page_links
