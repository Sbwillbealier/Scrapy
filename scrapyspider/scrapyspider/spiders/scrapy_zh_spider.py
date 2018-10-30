#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/10/29
@file:scrapy_zh_spider.py
@desc:
"""
from scrapy.spiders import Spider
import scrapy


class ScrapyZhSpider(Spider):
    name = 'scrapy_zh'

    # start_urls = ['http://lab.scrapyd.cn/']

    def start_requests(self):
        # 根据参数跟换url
        url = 'http://lab.scrapyd.cn/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            # 构造url若tag=爱情，url= "http://lab.scrapyd.cn/tag/爱情"
            url = url + 'tag/' + tag
        # 发送请求爬取参数内容
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        mingyans = response.css('div.quote')

        for mingyan in mingyans:
            text = mingyan.css('.text::text').extract_first()
            author = mingyan.css('.author::text').extract_first()
            tags = mingyan.css('.tags .tag::text').extract()
            tags = ','.join(tags)

            # 文件名
            filename = '%s-语录.txt' % (author)
            with open(filename, 'a+', encoding='utf-8') as f:
                f.write(text)
                f.write('\n')
                f.write('标签： ' + tags)
                f.write('\n--------\n')

        # 下一页
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            # 取出绝对路径
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
