import scrapy

from Steam.items import SteamItem
from .CONSTANT import Constant as c

class WegamespiderSpider(scrapy.Spider):
    name = 'wegamespider'
    allowed_domains = ['wegame.com.cn']

    base_url = "https://www.wegame.com.cn/store/games/mars_vars/page-"
    offset = 1
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//*[@class='game-item-list']/div")

        for node in node_list:
            item = SteamItem()
            item['game_src'] = 'WeGame'
            item['game_name'] = node.xpath("./div[1]/h3/span/text()").extract_first()
            item['game_img'] = "https:" + node.xpath("./a/div/img/@src").extract_first()
            tag_1 = node.xpath("./div[1]/div[2]/ul/li[1]/div/span/a/text()").extract_first()
            tag_2 = node.xpath("./div[1]/div[2]/ul/li[2]/div/span/a/text()").extract_first()
            tag_3 = node.xpath("./div[1]/div[2]/ul/li[3]/div/span/a/text()").extract_first()
            tag_4 = node.xpath("./div[1]/div[2]/ul/li[4]/div/span/a/text()").extract_first()
            if str(tag_1) != 'None':
                item['game_tag'] = str(tag_1) + ',' + str(tag_2) + ',' + str(tag_3) + ',' + str(tag_4)
            else:
                item['game_tag'] = "-"
            link = "https://www.wegame.com.cn" + node.xpath("./a/@href").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_detail,
                                 meta={'item': item})

        if self.offset < c.CNT_WEGAME:
            self.offset = self.offset + 1
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        link = str(response)[5:-1]

        item['game_link'] = link
        item['game_intro'] = response.xpath("//*[@id='game-detail-inner']/div/p/text()").extract_first()
        if not item['game_intro']:
            item['game_intro'] = "-"
        item['game_birth'] = response.xpath("//*[@class='detail-info']/div/ul/li[1]/div[2]/div/span/text()").extract_first()
        if not item['game_birth']:
            item['game_birth'] = "-"
        item['game_developer'] = response.xpath("//*[@class='detail-info']/div/ul/li[2]/div[2]/div/span/text()").extract_first()
        if not item['game_developer']:
            item['game_developer'] = "-"
        item['game_publisher'] = response.xpath("//*[@class='detail-info']/div/ul/li[3]/div[2]/div/span/text()").extract_first()
        if not item['game_publisher']:
            item['game_publisher'] = "-"

        yield item
