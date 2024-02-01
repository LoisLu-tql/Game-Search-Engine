import scrapy

from Steam.items import SteamItem


class UbisoftspiderSpider(scrapy.Spider):
    name = 'ubisoftspider'
    allowed_domains = ['ubisoft.com']
    start_urls = ['https://zh-cn.ubisoft.com/games']

    def parse(self, response):
        node_list = response.xpath("//*[@id='gamelist']/div")
        for node in node_list:
            item = SteamItem()
            item['game_src'] = 'Ubisoft'
            item['game_name'] = node.xpath("./div/div[2]/h3/text()").extract_first()
            item['game_img'] = node.xpath("./div/div[1]/a/img/@src").extract_first()
            item['game_birth'] = node.xpath("./div/div[2]/p/text()").extract_first()[5:]
            if not item['game_birth']:
                item['game_birth'] = "-"
            link = node.xpath("./div/div[1]/a/@href").extract_first()
            if(link[0] == '/'):
                link = "https://zh-cn.ubisoft.com" + link
            yield scrapy.Request(url=link, callback=self.parse_detail,
                                 meta={'item': item}, dont_filter=True)

    def parse_detail(self, response):
        item = response.meta['item']
        link = str(response)[5:-1]
        intro = ""

        item['game_link'] = link
        game_intros = response.xpath("//p/text()").extract()

        for game_intro in game_intros:
            intro = intro + game_intro
        item['game_intro'] = intro
        if not item['game_intro']:
            item['game_intro'] = "-"
        item['game_developer'] = '育碧'
        item['game_publisher'] = '育碧'
        item['game_tag'] = '-'
        yield item