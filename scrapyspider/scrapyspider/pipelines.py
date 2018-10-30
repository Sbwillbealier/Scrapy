# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        with open('douban.csv', 'a', encoding='utf-8') as f:
            f.write(item['ranking'])
            f.write(',')
            f.write(item['movie_name'])
            f.write(',')
            f.write(item['score'])
            f.write(',')
            f.write(item['score_num'])
            f.write(',')
            f.write('\n')
        return item
