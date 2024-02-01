# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name = scrapy.Field()
    game_link = scrapy.Field()
    game_img = scrapy.Field()
    game_intro = scrapy.Field()
    game_birth = scrapy.Field()
    game_developer = scrapy.Field()
    game_publisher = scrapy.Field()
    game_tag = scrapy.Field()
    game_src = scrapy.Field()
