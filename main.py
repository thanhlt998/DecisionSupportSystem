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


def main():
    nlp = NLP(TOKENIZER_PATH, MODEL_PATH)
    # Get search link
    search_url = 'https://store.steampowered.com/search?tags=19%2C21&category1=998'

    # Search
    setting = get_project_settings()
    setting['FEED_EXPORT_ENCODING'] = 'utf-8'
    configure_logging()
    runner = CrawlerRunner(setting)
    crawl(runner, search_url)
    reactor.run()

    # Classify
    nlp.classify_comments(NEW_GAMES_INFO_FN)

    # Import new game into database
    insert(CLASSIFIED_RESULT_FN)

    # TOPSIS
    matrix = turn_to_matrix()
    result = topsis(matrix, len(matrix), TOPSIS_WEIGHT, NO_ATTRIBUTES)
    print('Result: ', result)


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


if __name__ == '__main__':
    main()
