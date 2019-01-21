import requests
from bs4 import BeautifulSoup
from basic_operations import *
from global_vars import *


def scrape_poems(json_fname):
    pass


def scrape_urls(urls_fname):
    print("Scraping urls...")
    urls = list()
    basic_url = 'https://aconite26.livejournal.com/?skip={}&tag=стихи'
    step = 0
    while True:
        print("Step {}, {} urls so far".format(step, len(urls)))
        page = BeautifulSoup(requests.get(basic_url.format(step)).content,
                             'lxml').find_all('li', {'class': "asset-meta-likus item"})
        if not page:
            dump_utf_json(urls, urls_fname)
            return
        for item in page:
            urls.append(item.get('lj-likus-item'))
        step += 10


if __name__ == '__main__':
    scrape_urls(LJ_URLS_JSON)
