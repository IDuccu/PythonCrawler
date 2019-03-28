# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DmbjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
        section_name:分段名称
    """
    section_name = scrapy.Field()
    section_description = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_num = scrapy.Field()
    chapter_text = scrapy.Field()
    chapter_date = scrapy.Field()