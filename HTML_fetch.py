import requests
from bs4 import BeautifulSoup, Tag
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from process_HTML import ProcessHTML
import time

# This class opens the browser and navigates to the specified URL -> attempts to grab HTML contents of each page
class WebFetch:

    def __init__(self, max_pages=5,min_like_values = 5):
        self.min_like_values = min_like_values
        self.max_pages = max_pages
        self.setup()

    def get_web_content(self, url, waitMultiplier=1):
            infinite_scroll = True
            self.driver.get(url) # open brower and navigate to target url
            time.sleep(2 * waitMultiplier) # wait a little for stuff to load
            last_height = self.driver.execute_script("return document.body.scrollHeight") # get the height of the page
            for i in range(self.max_pages): # scroll down the page (many sites use infinite scrolling)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to bottom of page
                time.sleep(1 * waitMultiplier) # let new stuff load
                new_height = self.driver.execute_script("return document.body.scrollHeight") # check to see if the page height changes in response to scrolling
                if new_height == last_height: # if the height does not change it probably means that the page does not employ infinite scrolling
                    infinite_scroll = False
                    break # exit the loop so we dont waste time

            processer = ProcessHTML(url)

            if not infinite_scroll:
                HTML_buffer = []
                for i in range(self.max_pages):
                    processer.get_items(self.driver.page_source)
                    if not self.navigate_to_next_page():
                        break
                    time.sleep(1 * waitMultiplier)
            else:
                processer.get_items(self.driver.page_source)

            return processer.rep_elems
    
    def setup(self):
        self.options = webdriver.FirefoxOptions()
        self.options.binary_location = "./drivers/Firefox.app"
        self.options.add_argument("--headless=new") 
        self.driver = webdriver.Firefox(options=self.options)

    def end_session(self):
        self.driver.close()

    def get_items(self):
        self.traverse_tree(self.soup.body)

    def navigate_to_next_page(self):
        elements = self.driver.find_elements(By.TAG_NAME, 'a') # also consider selecting other elements if there are none 
        has_next_page = False
        for element in elements:
            text = element.text.lower().strip() # maybe also consider fuzzy text matching here instead
            if "next" in text:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
                has_next_page = True
                element.click()
                break
            else:
                pass # add identification of other common 'next page' arrows / buttons here
        
        return has_next_page
    
    def attempt_to_load_more(self):
        pass

    
    @classmethod
    def fetchHTML(cls, url, fake_headers=True):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        if fake_headers:
            resp = requests.get(url, headers=headers)
        else:
            resp = requests.get(url)

        if resp.status_code == 200:
            html_content = resp.text
            soup = BeautifulSoup(html_content, 'lxml')
            return soup
        
        else:
            print(f"Failed to fetch webpage. Status code: {resp.status_code}")
            return None
        
        
        


        