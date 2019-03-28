# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义爬取的数据结构
class TencentpositionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
        基准xpath: //tr[@class="even"] | //tr[@class="odd"]
        职位名称:   ./td[1]/a/text()
        职位链接:   ./td[1]/a/@href
        职位类别:   ./td[2]/text()
        招聘人数:   ./td[3]/text()
        工作地点:   ./td[4]/text()
        发布时间:   ./td[5]/text()
    """
    pos_name = scrapy.Field()
    pos_link = scrapy.Field()
    pos_type = scrapy.Field()
    pos_num = scrapy.Field()
    pos_city = scrapy.Field()
    pos_date = scrapy.Field()
    pos_detail = scrapy.Field()
