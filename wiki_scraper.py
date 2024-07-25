import requests
from bs4 import BeautifulSoup
import json


class WikiScraper:
    def __init__(self, url, cycles_number):
        self.url = url
        self.cycles_number = cycles_number
        self.visited_urls = set()
        self.links_to_visit = []
        self.scraped_links = {}

    def validate_wiki_link(self, link):
        if 'wikipedia.org' not in link:
            raise ValueError("The link is not a valid Wikipedia link.")
        if not 1 <= self.cycles_number <= 3:
            raise ValueError("The number of cycles should be between 1 and 3.")

    def scrape(self):
        self.validate_wiki_link(self.url)
        self.links_to_visit.append(self.url)

        for n in range(self.cycles_number):
            new_links = set()
            for link in self.links_to_visit:
                if link not in self.visited_urls:
                    self.visited_urls.add(link)
                    response = requests.get(link)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for a in soup.find_all('a', href=True):
                        if a['href'].startswith('/wiki') and ':' not in a['href']:
                            new_link = 'https://en.wikipedia.org' + a['href']
                            new_links.add(new_link)
            self.scraped_links[n + 1] = list(new_links)[:10]
            self.links_to_visit = list(new_links)

        with open('scraped_links.json', 'w') as file:
            json.dump(self.scraped_links, file, indent=4)


wiki_scraper = WikiScraper('https://en.wikipedia.org/wiki/Web_scraping', 2)
wiki_scraper.scrape()
