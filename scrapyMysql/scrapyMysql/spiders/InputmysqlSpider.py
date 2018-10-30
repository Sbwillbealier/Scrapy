# -*- coding: utf-8 -*-
import scrapy
from scrapyMysql.items import ScrapymysqlItem


class InputmysqlspiderSpider(scrapy.Spider):
    name = 'InputmysqlSpider'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/']

    def parse(self, response):
        mingyans = response.css('div.quote')

        item = ScrapymysqlItem()
        for mingyan in mingyans:
            text = mingyan.css('.text::text').extract_first()
            author = mingyan.css('.author::text').extract_first()
            tags = mingyan.css('.tags .tag::text').extract()
            tags = ','.join(tags)

            item['text'] = text
            item['author'] = author
            item['tags'] = tags

            yield item

        # 下一页
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
