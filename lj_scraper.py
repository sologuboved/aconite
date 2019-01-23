import re
import requests
from bs4 import BeautifulSoup
from basic_operations import *
from global_vars import *


@which_watch
def scrape_from_main(lj_main_json):
    print("Scraping urls...")
    from_main = list()
    basic_url = 'https://aconite26.livejournal.com/?skip={}&tag=стихи'
    step = 0
    while True:
        print("Step {}, {} urls so far".format(step, len(from_main)))
        page = BeautifulSoup(requests.get(basic_url.format(step)).content,
                             'lxml').find_all('h2', {'class': "asset-name page-header2"})
        if not page:
            dump_utf_json(from_main, lj_main_json)
            return
        for item in page:
            link = item.find('a', href=True)
            poem_datum = {SOURCE: link.get('href')}
            title = link.text.strip()
            if title == '***':
                poem_datum.update({TITLE: str(), WHEN: str()})
                from_main.append(poem_datum)
                continue
            when = title[-4:]
            try:
                int(when)
            except ValueError:
                when = str()
            else:
                title = str()
            poem_datum.update({TITLE: title, WHEN: when})
            from_main.append(poem_datum)
        step += 10


def add_lang_and_genre(soup, poem):
    user_tags = [item.text.strip() for item in soup.find('div', {'class': 'aentry-tags'}).find_all('a', href=True)]
    if "poems in english" in user_tags:
        poem[LANG] = ENG
    else:
        poem[LANG] = RUS
    poem[IS_TANKA] = "танки по дороге" in user_tags


if __name__ == '__main__':
    scrape_from_main(LJ_MAIN_JSON)
