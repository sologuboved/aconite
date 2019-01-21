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


# def scrape_poems(poems_json, ids_json):
#     pass


def scrape_poem(poem_id):
    source = 'https://aconite26.livejournal.com/{}.html'.format(poem_id)
    raw_poem = requests.get(source).content
    soup = BeautifulSoup(raw_poem, 'lxml')
    poem = {
        SOURCE: source,
        WHEN: '',
        WHERE: '',
        TITLE: soup.find('span', {'class': 'aentry-post__title-text'}).text.strip()
    }
    add_fields(soup, poem)
    get_text(raw_poem)
    print()
    return poem


def get_text(raw_poem):
    # print(str(raw_poem))
    # js = re.findall(r"Site\.page = (.+);\n\s*?Site.page.template", str(raw_poem))
    js = re.findall(r"Site\.page = (.+?);\\n\s*?Site\.page\.template", str(raw_poem))[0]
    print(js)
    json.loads(js)
    # print(json.loads(soup.find('script', {'type': 'text/javascript'}).text))
    # j = {"hasactiveuserpic": 0,
    #      "ajaxPagination": 1,
    #      "content": {"blocks": [{"entityRanges": [],
    #                              "text": "\xd0\x9f\xd0\xbe\xd0\xba\xd0\xbb\xd0\xbe\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5\\n\xd0\xa7\xd1\x91\xd1\x80\xd0\xbd\xd1\x8b\xd0\xbc \xd0\xb8\xd1\x80\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbc\\n\xd0\xa3\xd1\x82\xd1\x80\xd0\xbe\xd0\xbc \xd0\xbd\xd0\xb0 \xd1\x81\xd0\xba\xd0\xbb\xd0\xbe\xd0\xbd\xd0\xb5 \xd1\x85\xd0\xbe\xd0\xbb\xd0\xbc\xd0\xb0.\\n\xd0\x9e, \xd1\x82\xd0\xb0\xd0\xba\xd0\xbe\xd0\xb5, \xd1\x82\xd0\xb0\xd0\xba\xd0\xbe\xd0\xb5...\\n\xd0\xa2\xd1\x91\xd0\xbf\xd0\xbb\xd0\xbe\xd0\xb5 \xd1\x81\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x88\xd0\xb5\xd0\xbd\xd1\x81\xd1\x82\xd0\xb2\xd0\xbe.",
    #                              "type": "unstyled",
    #                              "data": {},
    #                              "depth": 0,
    #                              "key": "6b8f9",
    #                              "inlineStyleRanges": []},
    #                             {"entityRanges": [],
    #                              "text": " ",
    #                              "type": "atomic",
    #                              "data": {"width": 800,
    #                                       "originalSrc": "https://ic.pics.livejournal.com/aconite26/2649264/67627/67627_original.jpg",
    #                                       "src": "https://ic.pics.livejournal.com/aconite26/2649264/67627/67627_original.jpg",
    #                                       "fileName": "\xd0\x98\xd1\x80\xd0\xb8\xd1\x81\xd1\x8b3.jpg",
    #                                       "imageType": "standart",
    #                                       "originalWidth": 2560,
    #                                       "wHRatio": 1.77777777777778,
    #                                       "caption": "",
    #                                       "inheritPrivacy": 1,
    #                                       "class": "aentry-post__img--text-width",
    #                                       "type": "image",
    #                                       "id": "o_1ca3ukdcu11k8gnipuh10pfb8g"},
    #                              "depth": 0,
    #                              "key": "75a4o",
    #                              "inlineStyleRanges": []},
    #                             {"entityRanges": [],
    #                              "text": " ",
    #                              "type": "atomic",
    #                              "data": {"pairID": 1,
    #                                       "type": "lj-cut",
    #                                       "opening": 1},
    #                              "depth": 0,
    #                              "key": "f0j6n",
    #                              "inlineStyleRanges": []},
    #                             {"entityRanges": [],
    #                              "text": "\xd0\xa1\xd0\xbb\xd0\xb8\xd0\xb7\xd0\xbd\xd1\x83\xd0\xbb\xd0\xb0 \xd0\xba\xd0\xb0\xd0\xbf\xd0\xbb\xd1\x8e \\n\xd0\xa1\xd0\xb2\xd0\xb5\xd1\x82\xd0\xbb\xd0\xbe\xd0\xb9 \xd1\x80\xd0\xbe\xd1\x81\xd1\x8b \xd1\x81\xd0\xbe \xd1\x81\xd1\x82\xd0\xb5\xd0\xb1\xd0\xbb\xd1\x8f. \\n\xd0\x9e\xd0\xbd\xd0\xb0 \xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb4\xd0\xb0 \xd1\x81\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xba\xd0\xb0\xd1\x8f. \\n\xd0\xa2\xd0\xbe\xd0\xbc\xd0\xb8\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x87\xd0\xb8\xd1\x81\xd1\x82\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb9. \\n\xd0\x9a\xd0\xb0\xd0\xba \xd0\xb8\xd1\x85 \xd0\xb0\xd1\x80\xd0\xbe\xd0\xbc\xd0\xb0\xd1\x82.",
    #                              "type": "unstyled", "data": {}, "depth": 0, "key": "1sfst", "inlineStyleRanges": []},
    #                             {"entityRanges": [], "text": " ", "type": "atomic", "data": {"width": 800,
    #                                                                                          "originalSrc": "https://ic.pics.livejournal.com/aconite26/2649264/67961/67961_original.jpg",
    #                                                                                          "src": "https://ic.pics.livejournal.com/aconite26/2649264/67961/67961_original.jpg",
    #                                                                                          "fileName": "\xd0\x98\xd1\x80\xd0\xb8\xd1\x81\xd1\x8b1.jpg",
    #                                                                                          "imageType": "standart",
    #                                                                                          "originalWidth": 5120,
    #                                                                                          "wHRatio": 1.77777777777778,
    #                                                                                          "inheritPrivacy": 1,
    #                                                                                          "class": "aentry-post__img--text-width",
    #                                                                                          "type": "image",
    #                                                                                          "id": "o_1ca3umf4fpmdgi0cgp7e45prl"},
    #                              "depth": 0, "key": "da2h4", "inlineStyleRanges": []},
    #                             {"entityRanges": [], "text": "", "type": "unstyled", "data": {}, "depth": 0,
    #                              "key": "ep29j", "inlineStyleRanges": []},
    #                             {"entityRanges": [], "text": " ", "type": "atomic",
    #                              "data": {"pairID": 1, "type": "lj-cut", "opening": None}, "depth": 0, "key": "44e0u",
    #                              "inlineStyleRanges": []}], "entityMap": {}}, "comments": [
    #         {"userpic": "https://l-userpic.livejournal.com/119747978/57799953", "uname": "synchrozeta", "loaded": 1,
    #          "statprefix": "https://l-stat.livejournal.net", "deepLevel": 0, "talkid": 7194, "controls": None,
    #          "siteroot": "https://www.livejournal.com", "ipaddr": None, "parent": 0, "subject": "", "is_promo": 0,
    #          "username": [{"journal_url": "https://synchrozeta.livejournal.com/", "striked": None, "journaltype": "P",
    #                        "userhead_url": "https://l-stat.livejournal.net/img/userinfo_v8.svg?v=17080?v=294.2",
    #                        "color": None, "noctxpopup": 0, "side_alias": 0, "journal": "synchrozeta", "inline_css": 0,
    #                        "attrs": None, "is_identity": 0, "bold": 1, "show_userhead": 1, "username": "synchrozeta",
    #                        "user_alias": "", "profile_url": "https://synchrozeta.livejournal.com/profile", "alias": 0}],
    #          "thread": 1841864, "level": 1, "dname": "synchrozeta", "shown": 1, "collapsed": 0, "actions": [
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?replyto=1841864", "name": "reply",
    #              "title": "Reply", "footer": 1},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1841864#t1841864",
    #              "name": "permalink", "title": "link"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1841864#t1841864",
    #              "name": "collapse", "title": "Collapse"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1841864#t1841864",
    #              "name": "expand", "title": "Expand"}], "p_tracked": 0,
    #          "commenter_journal_base": "https://synchrozeta.livejournal.com/",
    #          "lj_statprefix": "https://l-stat.livejournal.net", "dtalkid": 1841864, "etime_ts": None,
    #          "thread_url": "https://aconite26.livejournal.com/240072.html?thread=1841864#t1841864", "above": None,
    #          "upictitle": "synchrozeta: pic#119747978",
    #          "article": "\xd0\x93\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xbb\xd0\xb8\xd1\x80\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xb8\xd0\xb9 \xd0\xb3\xd0\xb5\xd1\x80\xd0\xbe\xd0\xb9 \xd0\xb7\xd0\xb4\xd0\xb5\xd1\x81\xd1\x8c \xd0\xb2\xd1\x81\xd1\x91 \xd0\xb6\xd0\xb5 \xd0\xbd\xd0\xb5 \xd0\xb8\xd1\x80\xd0\xb8\xd1\x81\xd1\x8b, \xd0\x92\xd1\x8b \xd1\x87\xd1\x82\xd0\xbe-\xd1\x82\xd0\xbe \xd0\xb1\xd0\xbe\xd0\xbb\xd0\xb5\xd0\xb5 \xd0\xb8\xd0\xbd\xd1\x82\xd0\xb5\xd1\x80\xd0\xb5\xd1\x81\xd0\xbd\xd0\xbe\xd0\xb5 \xd0\xbd\xd0\xb0 \xd0\xb2\xd0\xb5\xd1\x80\xd1\x85\xd0\xbd\xd0\xb5\xd0\xbc \xd1\x84\xd0\xbe\xd1\x82\xd0\xbe \xd0\xbf\xd1\x80\xd0\xbe\xd0\xbf\xd1\x83\xd1\x81\xd1\x82\xd0\xb8\xd0\xbb\xd0\xb8)",
    #          "noid": None, "poster": "aconite26", "stime": "9 months ago", "below": None,
    #          "ctime": "April 2 2018, 21:03:47 UTC", "deleted_poster": None, "massactions": 0, "deleted": 0,
    #          "etime": None, "ctime_ts": 1522703027, "subclass": None, "suspended": None, "margin": 0, "leafclass": None,
    #          "is_best": 0, "tracked": 0},
    #         {"userpic": "https://l-userpic.livejournal.com/125991750/2649264", "uname": "aconite26", "loaded": 1,
    #          "statprefix": "https://l-stat.livejournal.net", "deepLevel": 0, "talkid": 7195, "controls": None,
    #          "siteroot": "https://www.livejournal.com", "ipaddr": None, "parent": 1841864, "subject": "", "is_promo": 0,
    #          "username": [{"journal_url": "https://aconite26.livejournal.com/", "striked": None, "journaltype": "P",
    #                        "userhead_url": "https://l-stat.livejournal.net/img/userinfo_v8.svg?v=17080?v=294.2",
    #                        "color": None, "noctxpopup": 0, "side_alias": 0, "journal": "aconite26", "inline_css": 0,
    #                        "attrs": None, "is_identity": 0, "bold": 1, "show_userhead": 1, "username": "aconite26",
    #                        "user_alias": "", "profile_url": "https://aconite26.livejournal.com/profile", "alias": 0}],
    #          "thread": 1842120, "level": 2, "dname": "aconite26", "shown": 1, "collapsed": 0, "actions": [
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?replyto=1842120", "name": "reply",
    #              "title": "Reply", "footer": 1},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842120#t1842120",
    #              "name": "permalink", "title": "link"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842120#t1842120",
    #              "name": "collapse", "title": "Collapse"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842120#t1842120",
    #              "name": "expand", "title": "Expand"}], "p_tracked": 0,
    #          "commenter_journal_base": "https://aconite26.livejournal.com/",
    #          "lj_statprefix": "https://l-stat.livejournal.net", "dtalkid": 1842120, "etime_ts": None,
    #          "thread_url": "https://aconite26.livejournal.com/240072.html?thread=1842120#t1842120", "above": 1841864,
    #          "upictitle": "Olga Kuminova: pic#125991750",
    #          "article": "\xd0\x9d\xd0\xb5 \xd1\x82\xd0\xb5\xd0\xbd\xd1\x8c \xd1\x81\xd0\xbb\xd1\x83\xd1\x87\xd0\xb0\xd0\xb9\xd0\xbd\xd0\xbe?",
    #          "noid": None, "poster": "aconite26", "stime": "9 months ago", "below": None,
    #          "ctime": "April 2 2018, 21:07:39 UTC", "deleted_poster": None, "massactions": 0, "deleted": 0,
    #          "etime": None, "ctime_ts": 1522703259, "subclass": None, "suspended": None, "margin": 30,
    #          "leafclass": None, "is_best": 0, "tracked": 0},
    #         {"userpic": "https://l-userpic.livejournal.com/119747978/57799953", "uname": "synchrozeta", "loaded": 1,
    #          "statprefix": "https://l-stat.livejournal.net", "deepLevel": 0, "talkid": 7196, "controls": None,
    #          "siteroot": "https://www.livejournal.com", "ipaddr": None, "parent": 1842120, "subject": "", "is_promo": 0,
    #          "username": [{"journal_url": "https://synchrozeta.livejournal.com/", "striked": None, "journaltype": "P",
    #                        "userhead_url": "https://l-stat.livejournal.net/img/userinfo_v8.svg?v=17080?v=294.2",
    #                        "color": None, "noctxpopup": 0, "side_alias": 0, "journal": "synchrozeta", "inline_css": 0,
    #                        "attrs": None, "is_identity": 0, "bold": 1, "show_userhead": 1, "username": "synchrozeta",
    #                        "user_alias": "", "profile_url": "https://synchrozeta.livejournal.com/profile", "alias": 0}],
    #          "thread": 1842376, "level": 3, "dname": "synchrozeta", "shown": 1, "collapsed": 0, "actions": [
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?replyto=1842376", "name": "reply",
    #              "title": "Reply", "footer": 1},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842376#t1842376",
    #              "name": "permalink", "title": "link"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842376#t1842376",
    #              "name": "collapse", "title": "Collapse"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842376#t1842376",
    #              "name": "expand", "title": "Expand"}], "p_tracked": 0,
    #          "commenter_journal_base": "https://synchrozeta.livejournal.com/",
    #          "lj_statprefix": "https://l-stat.livejournal.net", "dtalkid": 1842376, "etime_ts": None,
    #          "thread_url": "https://aconite26.livejournal.com/240072.html?thread=1842376#t1842376", "above": 1842120,
    #          "upictitle": "synchrozeta: pic#119747978",
    #          "article": "\xd0\x9d\xd0\xb5\xd1\x82. <br />\xd0\xa2\xd0\xbe, \xd1\x87\xd1\x82\xd0\xbe \xd1\x81\xd0\xba\xd1\x80\xd1\x8b\xd0\xb2\xd0\xb0\xd0\xb5\xd1\x82\xd1\x81\xd1\x8f \xd0\xb2 \xd1\x82\xd0\xb5\xd0\xbd\xd0\xb8.",
    #          "noid": None, "poster": "aconite26", "stime": "9 months ago", "below": None,
    #          "ctime": "April 2 2018, 21:11:31 UTC", "deleted_poster": None, "massactions": 0, "deleted": 0,
    #          "etime": None, "ctime_ts": 1522703491, "subclass": None, "suspended": None, "margin": 60,
    #          "leafclass": None, "is_best": 0, "tracked": 0},
    #         {"userpic": "https://l-userpic.livejournal.com/128567009/12690815", "uname": "dance_in_round", "loaded": 1,
    #          "statprefix": "https://l-stat.livejournal.net", "deepLevel": 0, "talkid": 7197, "controls": None,
    #          "siteroot": "https://www.livejournal.com", "ipaddr": None, "parent": 0, "subject": "", "is_promo": 0,
    #          "username": [
    #              {"journal_url": "https://dance-in-round.livejournal.com/", "striked": None, "journaltype": "P",
    #               "userhead_url": "https://l-stat.livejournal.net/img/userinfo_v8.svg?v=17080?v=294.2", "color": None,
    #               "noctxpopup": 0, "side_alias": 0, "journal": "dance_in_round", "inline_css": 0, "attrs": None,
    #               "is_identity": 0, "bold": 1, "show_userhead": 1, "username": "dance_in_round", "user_alias": "",
    #               "profile_url": "https://dance-in-round.livejournal.com/profile", "alias": 0}], "thread": 1842632,
    #          "level": 1, "dname": "dance_in_round", "shown": 1, "collapsed": 0, "actions": [
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?replyto=1842632", "name": "reply",
    #              "title": "Reply", "footer": 1},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842632#t1842632",
    #              "name": "permalink", "title": "link"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842632#t1842632",
    #              "name": "collapse", "title": "Collapse"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842632#t1842632",
    #              "name": "expand", "title": "Expand"}], "p_tracked": 0,
    #          "commenter_journal_base": "https://dance-in-round.livejournal.com/",
    #          "lj_statprefix": "https://l-stat.livejournal.net", "dtalkid": 1842632, "etime_ts": None,
    #          "thread_url": "https://aconite26.livejournal.com/240072.html?thread=1842632#t1842632", "above": None,
    #          "upictitle": "\xd0\x90\xd0\xbd\xd0\xbd\xd0\xb0: dreamer",
    #          "article": "*\xd0\xbc\xd0\xbe\xd0\xbb\xd1\x87\xd0\xb0 \xd0\xb2\xd0\xb7\xd0\xb4\xd0\xbe\xd1\x85\xd0\xbd\xd1\x83\xd0\xbb\xd0\xb0 \xd0\xbe\xd1\x82 \xd1\x80\xd0\xb0\xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd0\xb8 \xd1\x87\xd1\x83\xd0\xb6\xd0\xbe\xd0\xb3\xd0\xbe \xd1\x82\xd0\xb5\xd0\xbf\xd0\xbb\xd0\xb0*",
    #          "noid": None, "poster": "aconite26", "stime": "9 months ago", "below": None,
    #          "ctime": "April 3 2018, 06:32:56 UTC", "deleted_poster": None, "massactions": 0, "deleted": 0,
    #          "etime": None, "ctime_ts": 1522737176, "subclass": None, "suspended": None, "margin": 0, "leafclass": None,
    #          "is_best": 0, "tracked": 0},
    #         {"userpic": "https://l-userpic.livejournal.com/125991750/2649264", "uname": "aconite26", "loaded": 1,
    #          "statprefix": "https://l-stat.livejournal.net", "deepLevel": 0, "talkid": 7198, "controls": None,
    #          "siteroot": "https://www.livejournal.com", "ipaddr": None, "parent": 1842632, "subject": "", "is_promo": 0,
    #          "username": [{"journal_url": "https://aconite26.livejournal.com/", "striked": None, "journaltype": "P",
    #                        "userhead_url": "https://l-stat.livejournal.net/img/userinfo_v8.svg?v=17080?v=294.2",
    #                        "color": None, "noctxpopup": 0, "side_alias": 0, "journal": "aconite26", "inline_css": 0,
    #                        "attrs": None, "is_identity": 0, "bold": 1, "show_userhead": 1, "username": "aconite26",
    #                        "user_alias": "", "profile_url": "https://aconite26.livejournal.com/profile", "alias": 0}],
    #          "thread": 1842888, "level": 2, "dname": "aconite26", "shown": 1, "collapsed": 0, "actions": [
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?replyto=1842888", "name": "reply",
    #              "title": "Reply", "footer": 1},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842888#t1842888",
    #              "name": "permalink", "title": "link"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842888#t1842888",
    #              "name": "collapse", "title": "Collapse"},
    #             {"allowed": 1, "href": "https://aconite26.livejournal.com/240072.html?thread=1842888#t1842888",
    #              "name": "expand", "title": "Expand"}], "p_tracked": 0,
    #          "commenter_journal_base": "https://aconite26.livejournal.com/",
    #          "lj_statprefix": "https://l-stat.livejournal.net", "dtalkid": 1842888, "etime_ts": None,
    #          "thread_url": "https://aconite26.livejournal.com/240072.html?thread=1842888#t1842888", "above": 1842632,
    #          "upictitle": "Olga Kuminova: pic#125991750",
    #          "article": "\xd0\xbe\xd1\x85, \xd0\xb4\xd0\xb0.. \xd0\xb2\xd0\xbe\xd1\x82 \xd0\xb1\xd1\x8b \xd0\xbc\xd0\xbe\xd0\xb6\xd0\xbd\xd0\xbe \xd0\xb1\xd1\x8b\xd0\xbb\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8\xd1\x82\xd1\x8c\xd1\x81\xd1\x8f",
    #          "noid": None, "poster": "aconite26", "stime": "9 months ago", "below": None,
    #          "ctime": "April 4 2018, 20:58:20 UTC", "deleted_poster": None, "massactions": 0, "deleted": 0,
    #          "etime": None, "ctime_ts": 1522875500, "subclass": None, "suspended": None, "margin": 30,
    #          "leafclass": None, "is_best": 0, "tracked": 0}], "is_post": 1,
    #      "addfriend_link": "https://www.livejournal.com/subscribers/add?instant_relation=1&user=aconite26",
    #      "likes_signature": "ajax:1548064800:0::/_api/:2649264-240072:88c5bb86663482b3d342faa8c69122d5100280fa",
    #      "replycount": 5, "comments_page": 1, "scheme": "schemius",
    #      "adv_libs": {"google": {"url": "https://l-stat.livejournal.net/js/??ads/googletag.js?v=1547715431"},
    #                   "ssp": {"conflicts": ["adfox"]}, "inner": {}, "adfox": {"conflicts": ["ssp"], "url": None}},
    #      "D": {}, "is_images_migrated": False, "activeuserpic": "", "allow_commenting": 1, "ljtimes_min": 0,
    #      "add_ljlike": "1", "captcha_field_id": "capcode", "submitbtn_id": "comment_submit", "fotki": {
    #         "uploader": {"albumsData": [], "action": "add_new_post",
    #                      "privacyData": [{"groupname": "Everyone (Public)", "security": "public"},
    #                                      {"groupname": "Friends", "security": "allfriends"},
    #                                      {"groupname": "Just Me (Private)", "security": "private"}],
    #                      "tracking_opendialog": "tracking_photouploaded",
    #                      "sizesData": [{"is_default": 0, "text": "100", "size": "100"},
    #                                    {"is_default": 0, "text": "300", "size": "300"},
    #                                    {"is_default": 0, "text": "600", "size": "600"},
    #                                    {"is_default": 0, "text": "800", "size": "800"},
    #                                    {"is_default": 1, "text": "900", "size": "900"},
    #                                    {"is_default": 0, "text": "1000", "size": "1000"},
    #                                    {"is_default": 0, "text": "", "size": "2000"},
    #                                    {"is_default": 0, "text": "Original", "size": "original"}], "type": "upload",
    #                      "guid": ""}, "migration": 0, "upload": 0, "enabled": 0}, "hasdefaultuserpic": 0,
    #      "xc3_services_token": "46.188.125.204:1548068939:9088:60b03d40de8a2f484da7f2e2dee53891", "hasuserpics": 0,
    #      "spamcount": 0, "captcha_public": "6Ld6Ki0UAAAAAGJlOyw8jDevnSD6Z8ZknYZ1YOGc"}
    # dump_utf_json(j, 'j.json')
    # print(bytes(j['comments'][0]['article'], encoding='utf-8').decode("utf-8"))


def add_fields(soup, poem):
    user_tags = [item.text.strip() for item in soup.find('div', {'class': 'aentry-tags'}).find_all('a', href=True)]
    if "poems in english" in user_tags:
        poem[LANG] = ENG
    else:
        poem[LANG] = RUS
    poem[IS_TANKA] = "танки по дороге" in user_tags


if __name__ == '__main__':
    # scrape_ids(LJ_URLS_JSON)
    # print(scrape_poem('242261'))
    print(scrape_poem('240072'))
