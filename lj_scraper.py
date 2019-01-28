import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
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
                poem_datum.update({TITLE: str(), YEAR: str()})
                from_main.append(poem_datum)
                continue
            year = title[-4:]
            try:
                int(year)
            except ValueError:
                year = str()
            else:
                title = str()
            poem_datum.update({TITLE: title, YEAR: year})
            from_main.append(poem_datum)
        step += 10


@which_watch
def scrape_poems(lj_main_json, lj_poems_json):
    poems = load_utf_json(lj_main_json)
    total = len(poems)
    count = 0
    for poem in poems:
        count += 1
        print("\r{} / {}: {}".format(count, total, poem[SOURCE]), end='', flush=True)
        update_poem(poem)
    print('\nDumping...')
    dump_utf_json(poems, lj_poems_json)


def update_poem(poem):
    soup = BeautifulSoup(requests.get(poem[SOURCE]).content, 'lxml')
    raw_poem = soup.find('article', {'class': "b-singlepost-body entry-content e-content"})
    if raw_poem:
        tureen = soup
        b_type = True
    else:
        raw_poem = soup.find('article', {'class': 'aentry'})
        tureen = raw_poem
        b_type = False
    add_text(raw_poem, poem, b_type)
    add_lang_and_genre(tureen, poem, b_type)
    if not poem[YEAR]:
        add_year(tureen, poem, b_type)
    for fieldame in (MONTH, DAY):
        poem[fieldame] = str()


def add_text(raw_poem, poem, b_type):
    raw_poem = BeautifulSoup(re.sub(r"<br ?/?>", '\n', str(raw_poem)), 'lxml')
    if not b_type:
        raw_poem = raw_poem.find('div', {'class': 'aentry-post__text'})
    text = '\n\n'.join([paragraph.text.strip() for paragraph in raw_poem.find_all('p')])
    if not text:
        text = raw_poem.text
    poem[TEXT] = text.strip()


def add_year(tureen, poem, b_type):
    if b_type:
        poem[YEAR] = tureen.find('time').find('a', href=True).text
    else:
        poem[YEAR] = str(datetime.strptime(tureen.find('time').text, "%B %d %Y, %H:%M").year)


def add_lang_and_genre(tureen, poem, b_type):
    if b_type:
        user_tags = list()
        for item in tureen.find('div',
                                {'class': "b-singlepost-tags ljtags entry-content-asset p-category"}).find_all('a'):
            user_tags.append(item.text)
    else:
        user_tags = [item.text.strip() for item in tureen.find('div',
                                                               {'class': 'aentry-tags'}).find_all('a', href=True)]
    if "poems in english" in user_tags:
        poem[LANG] = ENG
    else:
        poem[LANG] = RUS
    poem[IS_TANKA] = "танки по дороге" in user_tags


if __name__ == '__main__':
    scrape_poems(LJ_MAIN_JSON, LJ_POEMS_JSON)
