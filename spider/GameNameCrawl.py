from scrapy import Request, Spider


class GameSpider(Spider):
    name = 'game_name'

    start_urls = [
        "https://store.steampowered.com/search/?term="
    ]

    selectors = {
        'game-link': "//div[@id='search_result_container']//a[contains(@class, 'search_result_row')]/@href",
        'game-name': "//*[@id='search_result_container']/div[2]/a/div[2]/div[1]/span/text()",
        'next-page': "//div[@class='search_pagination']//a[last()]/@href",
    }

    file = open('games.txt', mode='w', encoding='utf8')
    no_games = 0

    def parse(self, response):
        game_names = response.xpath(self.selectors['game-name']).getall()
        next_page = response.xpath(self.selectors['next-page']).get()

        for game_name in game_names:
            name = game_name.strip()
            if name != '':
                self.file.write(name + '\n')

        if next_page is not None:
            yield Request(url=next_page, callback=self.parse)

    def close(self, spider, reason):
        self.file.close()
