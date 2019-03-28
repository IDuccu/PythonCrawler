# -*- coding: utf-8 -*-
import json

import scrapy
from ..items import TencentpositionItem


class TencentpositionSpider(scrapy.Spider):
    name = 'tencentposition'
    allowed_domains = ['hr.tencent.com']
    # 基准url
    base_url = "https://hr.tencent.com/position.php?start="
    url = "https://hr.tencent.com/"
    # 初始页面值
    offset = 0
    # 起始url
    start_urls = [base_url + str(offset)]

    def parse(self, response):
        for i in range(0, 3090, 10):
            yield scrapy.Request(self.base_url + str(self.offset + i), callback=self.parse_html)

    def parse_html(self, response):
        # 每个职位节点对象列表
        base_xpath_lists = response.xpath('//tr[@class="even"] | //tr[@class="odd"]')
        for element in base_xpath_lists:
            item = TencentpositionItem()
            item['pos_name'] = element.xpath('./td[1]/a/text()').extract()[0]
            link = element.xpath('./td[1]/a/@href').extract()[0]
            item['pos_link'] = link
            pos_type = element.xpath('./td[2]/text()').extract()
            item['pos_type'] = pos_type[0] if pos_type else "无"
            item['pos_num'] = element.xpath('./td[3]/text()').extract()[0]
            item['pos_city'] = element.xpath('./td[4]/text()').extract()[0]
            item['pos_date'] = element.xpath('./td[5]/text()').extract()[0]
            yield scrapy.Request(self.url + link, meta={'item': item}, callback=self.parse_position_detail)

    def parse_position_detail(self, response):
        item = response.meta['item']
        detail = response.xpath('//ul[@class="squareli"]/li/text()').extract()
        item['pos_detail'] = '\n'.join(detail)
        yield item
