from scrapy import Spider, Request
import json
import re

from settings import *


class SearchResultsCrawler(Spider):
    name = "search_crawler"

    start_urls = [

    ]

    selectors = {
        "game_url": "//div[@id='search_result_container']//a[contains(@class, 'search_result_row')]/@href",
        "next_page": "//div[@class='search_pagination']//a[last()]/@href",
        "game": {
            "name": "//*[@id='search_result_container']/div[2]/a/div[2]/div[1]/span/text()",
            "price": "//*[@id='search_result_container']/div[2]/a/div[2]/div[4]/@data-price-final",
        }
    }

    max_no_result = MAX_NO_SEARCH_RESULT

    def __init__(self, name, **kwargs):
        self.name = name
        self.search_url = kwargs.get('search_url')
        self.output_file_name = kwargs.get('output_file_name')
        super(SearchResultsCrawler, self).__init__(name, **kwargs)

    def start_requests(self):
        yield Request(url=self.search_url, callback=self.parse_game_info)

    def parse(self, response):
        pass

    def parse_game_info(self, response):
        next_page = response.xpath(self.selectors['next_page']).get()
        no_game_in_page = len(response.xpath("//*[@id='search_result_container']/div[2]/a").getall())
        search_results = response.meta.setdefault('search_results', [])

        for i in range(no_game_in_page):
            game_url = response.xpath(
                f"//div[@id='search_result_container']//a[contains(@class, 'search_result_row')][{i + 1}]/@href").get()
            name = response.xpath(
                f"//*[@id='search_result_container']/div[2]/a[{i + 1}]/div[2]/div[1]/span/text()").get().strip()
            price = response.xpath(
                f"//*[@id='search_result_container']/div[2]/a[{i + 1}]/div[2]/div[4]/@data-price-final").get().strip()
            search_results.append({
                'url': game_url,
                'name': name,
                'price': price
            })

        if len(search_results) >= self.max_no_result:
            with open(self.output_file_name, mode='w', encoding='utf8') as f:
                json.dump(search_results[:self.max_no_result], f)
                f.close()
        elif next_page is not None:
            yield Request(url=next_page, callback=self.parse_game_info, meta={'search_results': search_results})


class NewGameInfoCrawler(Spider):
    name = "new_game_info_crawler"

    start_urls = [

    ]

    selectors = {
        "metacritic": {
            'url': "//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li/div/div[2]/div/h3/a/@href",
            "platform": "//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li/div/div[2]/div/p/span/text()",
            "comment": "//ol[@class='reviews user_reviews']/li/div/div/div/div/div/div[1]/div[2]//text()",
            "next_page": "//*[@id='main']/div[5]/div[2]/div/div[2]/div/div[1]/span[2]/a/@href",
            'metascore': "//*[@id='main']/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/a/div/span/text()",
            'userscore': "//*[@id='main']/div/div[3]/div/div/div[2]/div[1]/div[2]/div[1]/div/a/div/text()"
        }
    }

    new_game_info = [

    ]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'new_game_info.json',
        'DEPTH_PRIORITY': 1
    }

    def __init__(self, name, **kwargs):
        self.name = name
        self.new_game_list = kwargs.get('new_game_list')
        self.output_file_name = kwargs.get('output_file_name')
        super(NewGameInfoCrawler, self).__init__(name, **kwargs)

    def start_requests(self):
        if self.output_file_name is not None:
            self.custom_settings['FEED_URI'] = self.output_file_name
        for new_game in self.new_game_list:
            yield Request(url=self.create_metacritic_search_url(new_game['name']), callback=self.parse_game_info,
                          meta={'game': new_game})

    def parse(self, response):
        pass

    def parse_game_info(self, response):
        game = response.meta['game']

        no_result = len(response.xpath("//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li").getall())

        for i in range(no_result):
            url = response.xpath(
                f"//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li[{i + 1}]/div/div[2]/div/h3/a/@href").get()
            title = response.xpath(
                f"//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li[{i + 1}]/div/div[2]/div/h3/a/text()").get().strip()
            platform = response.xpath(
                f"//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li[{i + 1}]/div/div[2]/div/p/span/text()").get().strip()

            if re.sub(r'\s+', ' ', re.sub(r'\W', ' ', game['name']).lower()) == re.sub(r'\s+', ' ',
                                                                                       re.sub(r'\W', ' ',
                                                                                              title).lower()):
                game_tmp = game.copy()
                game_tmp['platform'] = platform
                yield Request(url=response.urljoin(url), callback=self.parse_score,
                              meta={"game": game_tmp})

    def parse_score(self, response):
        metascore = response.xpath(self.selectors['metacritic']['metascore']).get()
        userscore = response.xpath(self.selectors['metacritic']['userscore']).get()
        game = response.meta['game']
        try:
            game['metascore'] = int(metascore)
        except (TypeError, ValueError):
            game['metascore'] = 0

        try:
            game['userscore'] = float(userscore)
        except (TypeError, ValueError):
            game['userscore'] = 0
        yield Request(url=response.request.url + '/user-reviews', callback=self.parse_game_metacritic_comment,
                      meta={"game": game})

    def parse_game_metacritic_comment(self, response):
        next_page = response.xpath("//*[@id='main']/div[5]/div[2]/div/div[2]/div/div[1]/span[2]/a/@href").get()
        game = response.meta['game']
        comments = game.setdefault('comments', [])
        no_comment = len(response.xpath("//ol[@class='reviews user_reviews']/li").getall())
        for i in range(no_comment):
            comments.append(' '.join([comment.strip() for comment in response.xpath(
                f"//ol[@class='reviews user_reviews']/li[{i + 1}]/div/div/div/div/div/div[1]/div[2]//text()").getall()]))

        if next_page is not None:
            yield Request(url=response.urljoin(next_page), callback=self.parse_game_metacritic_comment,
                          meta={"game": game})
        else:
            yield game

    @staticmethod
    def create_metacritic_search_url(game):
        return f'https://www.metacritic.com/search/game/{game}/results'
