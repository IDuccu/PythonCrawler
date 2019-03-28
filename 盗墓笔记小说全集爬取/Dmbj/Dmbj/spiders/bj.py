# -*- coding: utf-8 -*-
import scrapy

from ..items import DmbjItem


class BjSpider(scrapy.Spider):
    name = 'bj'
    allowed_domains = ['daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    def parse(self, response):
        # 提取分段标题名称和链接
        base_xpath_list = response.xpath('//article//div[@class="homebook"]')
        link_xpath_list = response.xpath('//article//a')
        for element, link in zip(base_xpath_list, link_xpath_list):
            # 创建Item对象
            item = DmbjItem()
            item['section_name'] = element.xpath('./h2/text()').extract()[0]
            item['section_description'] = element.xpath(".//p[@class='homedes']/text()").extract()[0]
            sec_link = link.xpath('./@href').extract()[0]
            yield scrapy.Request(url=sec_link, meta={'item': item}, callback=self.parse_section)

    def parse_section(self, response):
        item = response.meta['item']
        base_xpath_list = response.xpath("//article[@class='excerpt excerpt-c3']")
        for element in base_xpath_list:
            # 解析章节名和章节数
            item['chapter_name'] = element.xpath("./a/text()").extract()[0]
            chap_link = element.xpath('./a/@href').extract()[0]
            yield scrapy.Request(url=chap_link, meta={'item': item}, callback=self.parse_chapter)

    def parse_chapter(self, response):
        item = response.meta['item']
        # 解析出更新时间和章节内容
        item['chapter_date'] = response.xpath('//div[@class="article-meta"]/span[1]/text()').extract()[0]
        # 解析章节内容
        item['chapter_text'] = '\n'.join(response.xpath('//article[@class="article-content"]/p/text()').extract())
        yield item
