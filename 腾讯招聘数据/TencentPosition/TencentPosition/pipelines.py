# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TencentpositionPipeline(object):
    def process_item(self, item, spider):
        # print("===============================")
        # print(item.get('pos_name'), item.get('pos_link'),
        #       item.get('pos_type'), item.get('pos_city'),
        #       item.get('pos_num'), item.get('pos_date'),
        #       item.get('pos_detail'), sep='\n')
        # print('===============================')
        return None