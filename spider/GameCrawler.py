from scrapy import Spider, Request
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
import re


class Crawler(Spider):
    name = 'game'

    start_urls = [
        'https://store.steampowered.com/search/?term='
    ]

    selectors = {
        "game_url": "//div[@id='search_result_container']//a[contains(@class, 'search_result_row')]/@href",
        "next_page": "//div[@class='search_pagination']//a[last()]/@href",
        "game": {
            "name": "//*[@id='search_result_container']/div[2]/a/div[2]/div[1]/span/text()",
            "price": "//*[@id='search_result_container']/div[2]/a/div[2]/div[4]/@data-price-final",
        },
        "metacritic": {
            'url': "//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li/div/div[2]/div/h3/a/@href",
            "platform": "//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li/div/div[2]/div/p/span/text()",
            "comment": "//ol[@class='reviews user_reviews']/li/div/div/div/div/div/div[1]/div[2]//text()",
            "next_page": "//*[@id='main']/div[5]/div[2]/div/div[2]/div/div[1]/span[2]/a/@href",
            'metascore': "//*[@id='main']/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div/a/div/span/text()",
            'userscore': "//*[@id='main']/div/div[3]/div/div/div[2]/div[1]/div[2]/div[1]/div/a/div/text()"
        }
    }

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 200,
        'DEPTH_PRIORITY': 1,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'game.json'
    }

    link_file = open('link_file.txt', mode='w', encoding='utf8')

    def parse(self, response):
        next_page = response.xpath(self.selectors['next_page']).get()
        no_game_in_page = len(response.xpath("//*[@id='search_result_container']/div[2]/a").getall())

        for i in range(no_game_in_page):
            game_url = response.xpath(f"//div[@id='search_result_container']//a[contains(@class, 'search_result_row')][{i + 1}]/@href").get()
            name = response.xpath(
                f"//*[@id='search_result_container']/div[2]/a[{i + 1}]/div[2]/div[1]/span/text()").get().strip()
            price = response.xpath(
                f"//*[@id='search_result_container']/div[2]/a[{i + 1}]/div[2]/div[4]/@data-price-final").get().strip()
            yield Request(url=self.create_metacritic_search_url(name), callback=self.parse_game_info,
                          meta={"url": game_url, "name": name, "price": price})

        if next_page is not None:
            self.link_file.write(next_page + '\n')
            yield Request(url=next_page, callback=self.parse)

    def parse_game_info(self, response):
        name = response.meta['name']
        price = response.meta['price']
        game_url = response.meta['url']

        no_result = len(response.xpath("//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li").getall())

        for i in range(no_result):
            url = response.xpath(
                f"//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li[{i + 1}]/div/div[2]/div/h3/a/@href").get()
            title = response.xpath(
                f"//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li[{i + 1}]/div/div[2]/div/h3/a/text()").get().strip()
            platform = response.xpath(
                f"//*[@id='main_content']/div[1]/div[3]/div[1]/ul/li[{i + 1}]/div/div[2]/div/p/span/text()").get().strip()

            if re.sub(r'\s+', ' ', re.sub(r'\W', ' ', name).lower()) == re.sub(r'\s+', ' ',
                                                                               re.sub(r'\W', ' ', title).lower()):
                game = {"url": game_url, "name": name, "price": price, "platform": platform}
                yield Request(url=response.urljoin(url), callback=self.parse_score,
                              meta={"game": game})

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

    def close(self, spider, reason):
        self.link_file.close()

    @staticmethod
    def create_metacritic_search_url(game):
        return f'https://www.metacritic.com/search/game/{game}/results'


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Crawler())
    process.start()
