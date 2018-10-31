# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from datetime import datetime


class ScrapybufanshangyePipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='scrapyMysql',
            user='root',
            password='root',
        )
        # 通过cursor执行正删改查
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # 存到测试数据库中
        self.cursor.execute(
            """insert into news(title, news.desc, thumbnail, content) values(%s, %s, %s, %s)""",
            (item['title'], item['desc'], item['thumbnail'], item['content'])
        )

        # 存到项目中
        # now = datetime.now()
        # self.cursor.execute(
        #     """insert into news_news(title, news_news.desc, thumbnail, content, pub_time, author_id, category_id) values(%s, %s, %s, %s, %s, "VGNccMzTogioX3zqWKc3si", 1)""",
        #     (item['title'], item['desc'], item['thumbnail'], item['content'], now)
        # )

        # 提交执行
        self.connect.commit()

        # 输出文件中
        # with open('news.txt', 'a+', encoding='utf-8') as f:
        #     f.write(item['title'])
        #     f.write('\n')
        #     f.write(item['desc'])
        #     f.write('\n')
        #     f.write(item['thumbnail'])
        #     f.write('\n')
        #     f.write(item['content'])
        #     f.write('\n-------\n')

        return item
