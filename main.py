from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
import json

from crawler import SearchResultsCrawler, NewGameInfoCrawler
from connect_db import *
from topsis import topsis
from NLP import NLP
from settings import *
import os
import tkinter as tk
from HQD import CheckbuttonList, get_search_link
import operator
import itertools
import collections

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def process(search_url, price, platform_list):
    print(search_url, price, platform_list)

    # Search
    setting = get_project_settings()
    setting['FEED_EXPORT_ENCODING'] = 'utf-8'
    setting['FEED_STORAGES_BASE'] = {
        '': 'custom_report_file.CustomFileFeedStorage',
        'file': 'custom_report_file.CustomFileFeedStorage',
    }
    configure_logging()
    runner = CrawlerRunner(setting)
    crawl(runner, search_url)
    reactor.run()

    # Classify
    if os.stat(NEW_GAMES_INFO_FN).st_size != 0:
        nlp.classify_comments(NEW_GAMES_INFO_FN)

        # Import new game into database
        insert(CLASSIFIED_RESULT_FN)

    # TOPSIS
    with open(SEARCH_RESULTS_FN, mode='r') as f:
        game_li = json.load(f)
        f.close()
    game_list = [game["name"] for game in game_li]
    print(len(game_list))
    matrix, id_list = turn_to_matrix(game_list, platform_list, price)
    result = topsis(matrix, len(matrix), TOPSIS_WEIGHT, NO_ATTRIBUTES)
    dictionary = dict(zip(id_list, result))
    dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    d = collections.OrderedDict(dictionary)
    x = itertools.islice(d.items(), 0, 4)
    key_list = []
    for key, value in x:
        key_list.append(key)
    res = select_game(key_list)
    print (res)
    try:
        os.remove(NEW_GAMES_INFO_FN)
        os.remove("search_results.json")
        os.remove("classified_result.json")
    except FileNotFoundError:
        print("")


def get_new_game_list(fn):
    with open(fn, mode='r') as f:
        game_list = json.load(f)
        f.close()

    existed_game_name = select_name()

    new_game_list = [game for game in game_list if game['name'] not in existed_game_name]

    return new_game_list


@defer.inlineCallbacks
def crawl(runner, search_url):
    yield runner.crawl(SearchResultsCrawler, name="search_crawler", search_url=search_url,
                       output_file_name=SEARCH_RESULTS_FN)

    # Load new game list
    new_game_list = get_new_game_list(SEARCH_RESULTS_FN)

    yield runner.crawl(NewGameInfoCrawler, name="new_game_info_crawler", new_game_list=new_game_list,
                       output_file_name=NEW_GAMES_INFO_FN)
    reactor.stop()


def main():
    root = tk.Tk()

    root.geometry('550x250')
    root.title("Game Picker")

    Type = GAME_TAGS.keys()
    Platform = ["PC", "XBox", "PS"]

    _type = CheckbuttonList(root, "Type", Type)
    _type.place(x=10, y=10)

    platform = CheckbuttonList(root, "Platform", Platform)
    platform.place(x=10, y=100)

    price = tk.Label(root, text="max price($)")
    price.place(x=10, y=150)
    _range = tk.Scale(root, from_=0, to=200, orient=tk.HORIZONTAL, length=500)
    _range.place(x=10, y=170)

    submit = tk.Button(root, text="Find", command=lambda: find(_range, _type, platform))
    submit.place(x=10, y=220)

    root.mainloop()


def find(_range, _type, platform):
    a = _range.get()
    type_list = _type.cb_values
    res_types = []
    for k, v in type_list.items():
        if v.get():
            res_types.append(k)

    platform_list = platform.cb_values
    res_platforms = []
    for k, v in platform_list.items():
        if v.get():
            res_platforms.append(k)

    process(search_url=get_search_link(res_types), price=a, platform_list=res_platforms)

if __name__ == '__main__':
    nlp = NLP(TOKENIZER_PATH, MODEL_PATH)
    main()
