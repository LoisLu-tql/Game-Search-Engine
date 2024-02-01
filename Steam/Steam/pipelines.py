# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
class SteamPipeline:
    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root', passwd='290102', db='games_db')
        self.cursor = self.connect.cursor()
        print("Connect to database successfully")

    def process_item(self, item, spider):
        sql = "insert into games(game_src, game_name, game_link, game_img, game_intro, game_birth, game_developer" \
              ", game_publisher, game_tag) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (item['game_src'], item['game_name'], item['game_link'], item['game_img'], item['game_intro']
                , item['game_birth'], item['game_developer'], item['game_publisher'], item['game_tag']))
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

