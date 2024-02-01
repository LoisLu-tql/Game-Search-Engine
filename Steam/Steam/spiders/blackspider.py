import scrapy

from Steam.items import SteamItem
from .CONSTANT import Constant as c

class BlackspiderSpider(scrapy.Spider):
    name = 'blackspider'
    allowed_domains = ['xiaoheihe.cn']

    base_url = "https://www.xiaoheihe.cn/games/rank/popular?page="
    offset = 1
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//*[@class='game-list']/ul/li")

        for node in node_list:
            item = SteamItem()
            item['game_src'] = '小黑盒'
            item['game_name'] = node.xpath("./a/div[2]/h3/text()").extract_first()
            item['game_img'] = node.xpath("./a/div[1]/img/@src").extract_first()
            link = "https://www.xiaoheihe.cn" + node.xpath("./a/@href").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_detail,
                                 meta={'item': item})

        if self.offset < c.CNT_BLACK:
            self.offset = self.offset + 1
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        link = str(response)[5:-1]

        item['game_link'] = link
        item['game_intro'] = response.xpath("//span[@class='desc']/text()").extract_first()
        if not item['game_intro']:
            item['game_intro'] = "-"
        item['game_birth'] = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[2]/p[1]/span[2]/text()").extract_first()
        if not item['game_birth']:
            item['game_birth'] = "-"
        item['game_developer'] = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[2]/p[2]/span[2]/text()").extract_first()
        if not item['game_developer']:
            item['game_developer'] = "-"
        item['game_publisher'] = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[2]/p[3]/span[2]/text()").extract_first()
        if not item['game_publisher']:
            item['game_publisher'] = "-"
        tag_1 = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[1]/span[1]/text()").extract_first()
        tag_2 = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[1]/span[2]/text()").extract_first()
        tag_3 = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[1]/span[3]/text()").extract_first()
        tag_4 = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[1]/span[4]/text()").extract_first()
        tag_5 = response.xpath("//*[@id='app']/div[2]/div/div[2]/div[2]/div[1]/span[5]/text()").extract_first()
        if(str(tag_1) != 'None'):
            item['game_tag'] = str(tag_1) + ',' + str(tag_2) + ',' + str(tag_3) + ',' + str(tag_4) + ',' + str(tag_5)
        else:
            item['game_tag'] = "-"
        yield item
