# -*- coding: utf-8 -*-
import scrapy
from scrapybufanshangye.items import ScrapybufanshangyeItem
import json


class BufanshangyeSpider(scrapy.Spider):
    name = 'BuFanShangYe'
    # allowed_domains = ['https://www.bufanbiz.com/']
    start_urls = ['https://www.bufanbiz.com/']

    def parse(self, response):
        newses = response.css('ul.news-list li')

        item = ScrapybufanshangyeItem()
        for news in newses:
            item['title'] = news.css('div.li-title::text').extract_first()
            item['desc'] = news.css('div.li-detail::text').extract_first()
            item['thumbnail'] = news.css('.li-img img::attr(src)').extract_first()
            # 获取详情页url
            content_url = news.css('a.li-container::attr(href)').extract_first()
            content_url = response.urljoin(content_url)
            # 把item传到详情页去
            yield scrapy.Request(url=content_url, callback=self.parse_detail_info, meta=item)

        # 加载更多
        more_news = response.css('div.more-news')
        if more_news is not None:
            # 动态请求 p：页码；n：每页新闻数
            ajax_url = response.urljoin('api/website/articles/?p=3&n=20&type=')
            yield scrapy.Request(url=ajax_url, callback=self.parse_json)

    def parse_detail_info(self, response):
        item = response.meta  # 接收列表模型
        content = response.css('div.content-detail').extract_first().split('\n')[1].strip()
        item['content'] = content.encode('gbk', 'ignore').decode('gbk')
        # print(item['content'])
        yield item

    def parse_json(self, response):
        # 解析json文件
        newses_json = json.loads(response.body_as_unicode())
        newses_json = newses_json['data']

        item = ScrapybufanshangyeItem()
        for news in newses_json:
            item['title'] = news['title']
            item['desc'] = news['intro']
            item['thumbnail'] = news['photo']

            # 详情
            news_id = news['uid']
            url = 'https://www.bufanbiz.com/post/%s.html' % news_id
            yield scrapy.Request(url=url, callback=self.parse_detail_info, meta=item)
