import re
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


@which_watch
def scrape_poems(ids_json, poems_json):
    poems = list()
    suspicious = list()
    poem_ids = load_utf_json(ids_json)
    total = len(poem_ids)
    count = 0
    for poem_id in poem_ids:
        count += 1
        print("\r{} / {}: {}".format(count, total, poem_id), end='', flush=True)
        poem = scrape_poem(poem_id)
        if poem:
            poems.append(poem)
        else:
            suspicious.append(poem_id)
    dump_utf_json(poems, poems_json)


def scrape_poem(poem_id):
    source = 'https://aconite26.livejournal.com/{}.html'.format(poem_id)
    soup = BeautifulSoup(requests.get(source).content, 'lxml')
    try:
        title = soup.find('span', {'class': 'aentry-post__title-text'}).text.strip()
    except AttributeError:
        title = str()
    if title == 'Книга':
        return
    poem = {
        SOURCE: source,
        WHEN: str(),
        WHERE: str(),
        TITLE: title,
        TEXT: get_text(soup)
    }
    add_lang_and_genre(soup, poem)
    return poem


def add_text_and_title(soup, poem):
    raw_text = re.findall(r"Site\.page = (.+?\});\s+Site.page.template",
                          str(soup.find_all('script', {'type': 'text/javascript'})[2]))[0]
    # print(raw_text)
    text = '\n\n'.join(
        [item['text'].strip() for item in json.loads(raw_text)['content']['blocks'] if item['text'].strip()])
    # print(repr(text))
    poem[TEXT] = text


def add_lang_and_genre(soup, poem):
    user_tags = [item.text.strip() for item in soup.find('div', {'class': 'aentry-tags'}).find_all('a', href=True)]
    if "poems in english" in user_tags:
        poem[LANG] = ENG
    else:
        poem[LANG] = RUS
    poem[IS_TANKA] = "танки по дороге" in user_tags


if __name__ == '__main__':
    # scrape_ids(LJ_IDS_JSON)
    # scrape_poem('242261')
    # print(scrape_poem('240072'))
    scrape_poems(LJ_IDS_JSON, LJ_POEMS_JSON)
