#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/10/30
@file:MySQLPipeline.py
@desc:
"""
import pymysql


# 编写MySQL存储插件：MySQLPipeline.py
class MySQLPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='106.14.173.118',
            port=3306,
            db='scrapyMysql',
            user='root',
            password='root',
        )
        # 通过cursor执行正删改查
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into mingyan(text, author, tags) value(%s, %s, %s)""",
            (item['text'],
             item['author'],
             item['tags'],))
        # 提交执行
        self.connect.commit()
        # 下面也必须返回
        return item
