# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DmbjPipeline(object):
    def process_item(self, item, spider):
        """返回json格式文件并写入文件"""
        js = {
            "section_name": item.get("section_name", ''),
            'section_description': item.get("section_description", ""),
            "details": {
                'chapter_name': item.get('chapter_name', ""),
                'chapter_date': item.get("chapter_date", ""),
                'chapter_text': item.get('chapter_text', ""),
            }
        }

        j_str = json.dumps(js, ensure_ascii=False)
        with open('dmbj.txt', 'a', encoding='utf-8') as f:
            f.write(j_str+"\n")

