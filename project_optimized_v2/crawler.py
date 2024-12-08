from urllib.request import urlopen
from urllib.parse import urljoin, urlparse
from db_connection_mongo import *
from bs4 import BeautifulSoup
import re

class Frontier:
    def __init__(self, url):
        parse_res = urlparse(url)
        self.base_url = parse_res.scheme + '://' + parse_res.netloc + '/index.shtml'
        self.urls = [
            cleanURL(self.base_url, url)
        ]

    def done(self):
        return not self.urls

    def nextURL(self):
        self.base_url = self.urls.pop(0)
        return self.base_url
    
    def addURL(self, url):
        url = cleanURL(self.base_url, url)
        page = findPage(pages, { "url": url })
        if not page and not url in self.urls:
            self.urls.append(url)

    def clear(self):
        self.urls.clear()

def cleanURL(base_url, url):
    if not url.endswith('.shtml'):
        url = urljoin(url, "index.shtml")
    return urljoin(base_url, url.replace('~', '').removesuffix('index.shtml'))

def retrieveHTML(url):
        try:
            with urlopen(url) as response:
                if 'text/html' not in response.getheader('Content-Type', ''):
                    return None, 'not text/html'
                return response.read().decode('utf-8'), 'success'
        except Exception as e:
            return None, str(e)

def parse(html):
    try:
        bs = BeautifulSoup(html, 'html.parser')
        regex = re.compile(r'^((https?:\/\/)?www\.cpp\.edu)?\/?[^\.\n#]*(\.s?html)?$')
        return {
            'isTargetPage': not not bs.find('div', { 'class': 'fac-info' }),
            'hrefs': [a.get('href') for a in bs.find_all('a', { 'href': regex })]
        }
    except Exception:
        return {
            'isTargetPage': False,
            'hrefs': []
        }

def storePage(url, html, status_message):
    page = findPage(pages, { "url": url })
    if not page:
        createPage(pages, url, html, status_message)

def flagTargetPage(url):
    page = findPage(pages, { "url": url })
    if page:
        flagPage(pages, url)

def crawlerThread(frontier: Frontier, num_targets: int = 22):
    targets_found = 0
    while not frontier.done():
        url = frontier.nextURL()
        html, status_message = retrieveHTML(url)
        storePage(url, html, status_message)
        parsedHTML = parse(html)
        if parsedHTML['isTargetPage']:
            flagTargetPage(url)
            targets_found += 1
        if targets_found == num_targets:
            frontier.clear()
        else:
            for a_href in parsedHTML['hrefs']:
                frontier.addURL(a_href)

if __name__ == "__main__":
    db = connectDataBase()
    pages = db["pages"]
    pages.drop()
    crawlerThread(Frontier("https://www.cpp.edu/cba/international-business-marketing/index.shtml"), -1)