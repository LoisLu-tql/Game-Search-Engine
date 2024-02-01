import scrapy
from .CONSTANT import Constant as c
from ..items import SteamItem


class ThreedmspiderSpider(scrapy.Spider):
    name = 'ThreeDMspider'
    allowed_domains = ['shop.3dmgame.com']

    base_url = "https://shop.3dmgame.com/game_all/?page="
    offset = 1
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = response.xpath("/html/body/div[2]/div[1]/div[4]/ul/li")

        for node in node_list:
            item = SteamItem()
            item['game_src'] = '3DM'
            item['game_name'] = node.xpath("./div/a/text()").extract_first()
            item['game_img'] = node.xpath("./a/img/@src").extract_first()
            link = node.xpath("./div/a/@href").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_detail,
                                 meta={'item': item}, dont_filter=True)

        if self.offset < c.CNT_3DM:
            self.offset = self.offset + 1
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        link = str(response)[5:-1]

        item['game_link'] = link
        item['game_intro'] = response.xpath("//*[@class='news_infor ']/p/text()").extract_first()
        if not item['game_intro']:
            item['game_intro'] = "-"
        item['game_birth'] = response.xpath("//*[@class='text_box']/div[2]/span[4]/text()").extract_first()[5:]
        if not item['game_birth']:
            item['game_birth'] = "-"
        item['game_developer'] = response.xpath("//*[@class='text_box']/div[2]/span[2]/text()").extract_first()[5:]
        if not item['game_developer']:
            item['game_developer'] = "-"
        item['game_publisher'] = response.xpath("//*[@class='text_box']/div[2]/span[2]/text()").extract_first()[5:]
        if not item['game_publisher']:
            item['game_publisher'] = "-"
        item['game_tag'] = response.xpath("//*[@class='text_box']/div[2]/span[1]/text()").extract_first()[5:]
        if not item['game_tag']:
            item['game_tag'] = "-"
        yield item

        #//*[@id="app"]/div[2]/div/div[5]/div[2]/div/div[1]/ul
        #//*[@id="dvContent"]/div/div[2]/div/div[1]/div/div/div/ul[1]/li[1]/div/div[1]/h3/span