import requests
from bs4 import BeautifulSoup
from basic_operations import *
from global_vars import *


def scrape_ids(ids_json):
    print("Scraping urls...")
    ids = list()
    basic_url = 'https://aconite26.livejournal.com/?skip={}&tag=стихи'
    step = 0
    while True:
        print("Step {}, {} urls so far".format(step, len(ids)))
        page = BeautifulSoup(requests.get(basic_url.format(step)).content,
                             'lxml').find_all('li', {'class': "asset-meta-likus item"})
        if not page:
            dump_utf_json(ids, ids_json)
            return
        for item in page:
            ids.append(item.get('lj-likus-item'))
        step += 10


def scrape_poems(poems_json, ids_json):
    pass


def scrape_poem(poem_id):
    soup = BeautifulSoup(requests.get('https://aconite26.livejournal.com/{}.html'.format(poem_id)).content, 'lxml')


if __name__ == '__main__':
    scrape_ids(LJ_URLS_JSON)
    scrape_poem('243689')
