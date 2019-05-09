import scrapy
from scrapy import Request
import re
import math


class CommentSpider(scrapy.Spider):
    name = 'steam_comment'

    start_urls = [
        "https://store.steampowered.com/search/?term=",
    ]

    selectors = {
        'game-link': "//div[@id='search_result_container']//a[contains(@class, 'search_result_row')]/@href",
        'next-page': "//div[@class='search_pagination']//a[last()]/@href",
        'comment': "//div[contains(@class,'modalContentLink interactable')]/div[@class='apphub_CardContentMain']/div[@class='apphub_UserReviewCardContent']/div[@class='apphub_CardTextContent']/text()",
        'no_positive_comments': "//div[@id='reviews_filter_options']/div[@class='user_reviews_filter_menu']//label[@for='review_type_positive']/span/text()",
        'no_negative_comments': "//div[@id='reviews_filter_options']/div[@class='user_reviews_filter_menu']//label[@for='review_type_negative']/span/text()"
    }

    negative_file = open('negative_comment.txt', mode='a', encoding='utf8')
    positive_file = open('positive_comment.txt', mode='a', encoding='utf8')
    no_positive_comments = 0
    no_negative_comments = 0
    no_request = 0

    def parse(self, response):
        game_link_list = response.xpath(self.selectors['game-link']).getall()
        next_page = response.xpath(self.selectors['next-page']).get()

        for link in game_link_list:
            yield Request(url=link, callback=self.parse_comments)

        if next_page is not None and self.no_request < 20000:
            yield Request(url=next_page, callback=self.parse)

    def parse_comments(self, response):
        game_id = response.request.url.split("/")[4]
        # no_cmts = response.xpath(self.selectors['no_positive_comments']).get()
        no_cmts = response.xpath(self.selectors['no_negative_comments']).get()
        if no_cmts is None:
            return
        # no_positive_comments = int(''.join(re.compile('\d+').findall(no_cmts)))
        no_negative_comments = int(''.join(re.compile('\d+').findall(no_cmts)))

        # for i in range(1, math.ceil(no_positive_comments/10)):
        #     if self.no_request > 20000:
        #         return
        #     yield Request(url=self.get_positive_comment_link(game_id=game_id, page_num=i), callback=self.parse_positive_comments)
        #     self.no_request += 1

        for i in range(1, math.ceil(no_negative_comments/10)):
            if self.no_request > 50000:
                return
            yield Request(url=self.get_negative_comment_link(game_id=game_id, page_num=i), callback=self.parse_negative_comments)
            self.no_request += 1



    def parse_positive_comments(self, response):
        for i in range(1, len(response.xpath("//div[contains(@class,'modalContentLink interactable')]")) + 1):
            comments = response.xpath(f"//div[contains(@class,'modalContentLink interactable')][{i}]/div[@class='apphub_CardContentMain']/div[@class='apphub_UserReviewCardContent']/div[@class='apphub_CardTextContent']/text()").getall()
            text = ' '.join([s.strip() for s in comments])
            if text != '':
                self.positive_file.write(text + '\n')
                self.no_positive_comments += 1

    def parse_negative_comments(self, response):
        for i in range(1, len(response.xpath("//div[contains(@class,'modalContentLink interactable')]")) + 1):
            comments = response.xpath(f"//div[contains(@class,'modalContentLink interactable')][{i}]/div[@class='apphub_CardContentMain']/div[@class='apphub_UserReviewCardContent']/div[@class='apphub_CardTextContent']/text()").getall()
            text = ' '.join([s.strip() for s in comments])
            if text != '':
                self.negative_file.write(text + '\n')
                self.no_negative_comments += 1

    def get_positive_comment_link(self, game_id, page_num):
        return f'https://steamcommunity.com/app/{game_id}/homecontent/?userreviewsoffset={(page_num - 1) * 10}&p={page_num}&workshopitemspage={page_num}&readytouseitemspage={page_num}&mtxitemspage={page_num}&itemspage={page_num}&screenshotspage={page_num}&videospage={page_num}&artpage={page_num}&allguidepage={page_num}&webguidepage={page_num}&integratedguidepage={page_num}&discussionspage={page_num}&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid={game_id}&appHubSubSection=16&appHubSubSection=16&l=english&filterLanguage=default&searchText=&forceanon=1'

    def get_negative_comment_link(self, game_id, page_num):
        return f'https://steamcommunity.com/app/{game_id}/homecontent/?userreviewsoffset={(page_num - 1) * 10}&p={page_num}&workshopitemspage={page_num}&readytouseitemspage={page_num}&mtxitemspage={page_num}&itemspage={page_num}&screenshotspage={page_num}&videospage={page_num}&artpage={page_num}&allguidepage={page_num}&webguidepage={page_num}&integratedguidepage={page_num}&discussionspage={page_num}&numperpage=10&browsefilter=toprated&browsefilter=toprated&appid={game_id}&appHubSubSection=17&appHubSubSection=17&l=english&filterLanguage=default&searchText=&forceanon=1'

    def close(self, spider, reason):
        self.negative_file.close()
        self.positive_file.close()
        print(f'Crawled {self.no_positive_comments} positive comments and {self.no_negative_comments} negative comments.')
