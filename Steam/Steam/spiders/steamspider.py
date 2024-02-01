import scrapy
from Steam.items import SteamItem
from .CONSTANT import Constant as c

class SteamspiderSpider(scrapy.Spider):
    name = 'steamspider'
    allowed_domains = ['steampowered.com']

    base_url = "https://store.steampowered.com/search/?language=chinese&page="
    offset = 1
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//*[@id='search_resultsRows']/a")

        for node in node_list:
            item = SteamItem()
            item['game_src'] = 'Steam'
            item['game_name'] = node.xpath("./div[2]/div[1]/span/text()").extract_first()
            item['game_img'] = node.xpath("./div[1]/img/@src").extract_first()
            link = node.xpath("./@href").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_detail,
                                 meta={'item': item})

        if self.offset < c.CNT_STEAM:
            self.offset = self.offset + 1
            url = self.base_url + str(self.offset)
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        link = str(response)[5:-1]

        item['game_link'] = link
        item['game_intro'] = response.xpath("//*[@id='game_highlights']/div[1]/div/div[2]/text()").extract_first()
        if not item['game_intro']:
            item['game_intro'] = "-"
        item['game_birth'] = response.xpath("//*[@id='game_highlights']/div[1]/div/div[3]/div[2]/div[2]/text()").extract_first()
        if not item['game_birth']:
            item['game_birth'] = "-"
        item['game_developer'] = response.xpath("//*[@id='developers_list']/a/text()").extract_first()
        if not item['game_developer']:
            item['game_developer'] = "-"
        item['game_publisher'] = response.xpath("//*[@id='game_highlights']/div[1]/div/div[3]/div[4]/div[2]/a/text()").extract_first()
        if not item['game_publisher']:
            item['game_publisher'] = "-"
        tag_1 = response.xpath("//*[@id='glanceCtnResponsiveRight']/div[2]/div[2]/a[1]/text()").extract_first()
        tag_2 = response.xpath("//*[@id='glanceCtnResponsiveRight']/div[2]/div[2]/a[2]/text()").extract_first()
        tag_3 = response.xpath("//*[@id='glanceCtnResponsiveRight']/div[2]/div[2]/a[3]/text()").extract_first()
        tag_4 = response.xpath("//*[@id='glanceCtnResponsiveRight']/div[2]/div[2]/a[4]/text()").extract_first()
        tag_5 = response.xpath("//*[@id='glanceCtnResponsiveRight']/div[2]/div[2]/a[5]/text()").extract_first()
        if(str(tag_1) != 'None'):
            item['game_tag'] = str(tag_1) + ',' + str(tag_2) + ',' + str(tag_3) + ',' + str(tag_4) + ',' + str(tag_5)
        else:
            item['game_tag'] = "-"
        yield item