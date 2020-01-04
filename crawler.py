#! /usr/local/bin/python3

import sys
import requests
import re
from urllib.parse import urlparse

class Crawler(object):    
    def __init__(self, start_url):    
        self.start_url = start_url             
        self.links_set = set()

    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ''
        return html.content.decode('utf-8')

    def get_all_links(self, url):
        html = self.get_html(url)
        links = re.findall(r'<a(?:[^>]*?\s+)?href="([^"]*)"', html)
        parsed = urlparse(url)
        base = F"{parsed.scheme}://{parsed.netloc}"

        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                links[i] = base + link

        return set(filter(lambda x: 'mailto' not in x, links))

    def crawl(self, url):
        for link in self.get_all_links(url):
            if link in self.links_set:
                continue
            print(link)
            self.links_set.add(link)
            self.crawl(link)

    def start(self):
        self.crawl(self.start_url)

if __name__ == '__main__':   
    site = sys.argv[1]
    if 'http' not in site:
        site = 'http://' + site
    crawler = Crawler(site)
    crawler.start()
