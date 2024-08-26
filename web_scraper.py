import logging
import time
from urllib.parse import urljoin, urlparse
from typing import Set, Generator, Tuple
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

class EnhancedWebScraper:
    def __init__(self, base_url: str, delay: float = 1, use_selenium: bool = False, max_pages: int = 100):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.delay = delay
        self.visited = set()
        self.use_selenium = use_selenium
        self.max_pages = max_pages
        self.driver = None
        if self.use_selenium:
            self._setup_selenium()

    def _setup_selenium(self):
        logging.info("Setting up Selenium with Chromium")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.binary_location = "/snap/bin/chromium"
        
        logging.info("Initializing Chromium WebDriver")
        try:
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                options=chrome_options
            )
            logging.info("Chromium WebDriver initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Chromium WebDriver: {str(e)}", exc_info=True)
            raise

    def get_page_content(self, url: str) -> str:
        if self.use_selenium:
            self.driver.get(url)
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                return self.driver.page_source
            except Exception as e:
                logging.error(f"Error loading page {url}: {str(e)}")
                return ""
        else:
            response = requests.get(url, headers={'User-Agent': 'Custom Web Scraper 1.0'})
            response.raise_for_status()
            return response.text

    def extract_links(self, url: str, content: str) -> Set[str]:
        soup = BeautifulSoup(content, 'html.parser')
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            if urlparse(full_url).netloc == self.domain:
                links.add(full_url)
        return links

    def process_sitemap(self, sitemap_url: str) -> Set[str]:
        try:
            response = requests.get(sitemap_url, headers={'User-Agent': 'Custom Web Scraper 1.0'})
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            urls = set()
            # Process sitemap index
            for sitemap in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                if sitemap.text.endswith('.xml'):
                    urls.update(self.process_sitemap(sitemap.text))
                else:
                    urls.add(sitemap.text)
            
            # Process regular sitemap
            for url in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                urls.add(url.text)
            
            return urls
        except Exception as e:
            logging.error(f"Failed to process sitemap {sitemap_url}: {str(e)}")
            return set()

    def crawl(self, use_sitemap: bool = False) -> Generator[Tuple[str, str], None, None]:
        to_visit = set([self.base_url])
        if use_sitemap:
            sitemap_url = urljoin(self.base_url, "sitemap.xml")
            to_visit.update(self.process_sitemap(sitemap_url))

        while to_visit and len(self.visited) < self.max_pages:
            url = to_visit.pop()
            if url in self.visited:
                continue

            try:
                content = self.get_page_content(url)
                if content:
                    self.visited.add(url)
                    yield url, content

                    if not use_sitemap:
                        new_links = self.extract_links(url, content)
                        to_visit.update(new_links - self.visited)

                time.sleep(self.delay)
            except Exception as e:
                logging.error(f"Failed to process {url}: {str(e)}")

    def close(self):
        if self.driver:
            self.driver.quit()