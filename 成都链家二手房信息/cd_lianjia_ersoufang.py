"""本程序示例示意爬取成都链家二手房信息并写入csv文件或mysql
    url : https://cd.lianjia.com/ershoufang/
"""
import random
import warnings

import pymysql
import requests
import re
import time
import csv


class LianjiaSpider:
    def __init__(self):
        self.base_url = "https://cd.lianjia.com/ershoufang/pg"
        self.headers = {
            "User-Agent": "(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/72.0.3626.121 Safari/537.36"
        }
        # 使用代理
        self.proxies = {}
        self.page = 0
        self.filename = '链家.csv'

        # 连接到数据库
        self.db = pymysql.connect('localhost', 'root',
                                  "123456", charset="utf8")

    # 获取页面信息
    def get_page(self, url):
        res = requests.get(url, headers=self.headers, proxies=self.proxies)
        res.encoding = 'utf-8'
        html = res.text
        self.parse_page(html)

    # 解析页面并提取数据
    def parse_page(self, html):
        """爬取的信息有:
            小区: h_name
            面积: h_size
            房型: h_type
            装修: h_dec
            单价: h_sPrice
            房价: h_price
            r_list格式: [(h_name, h_type, h_size, h_dec, h_price, h_sPrice)]
        """
        patterns = '<div class="houseInfo">[\s\S]*?="region">([\s\S]*?) </a> \|(.*?) \|(.*?)平米 \|.*?\|(.*?)[\||<|]' \
                   '[\s\S]*?<div class="totalPrice"><span>([\s\S]*?)</span>[\s\S]*?<span>单价(.*?)元'
        p = re.compile(patterns, re.S)
        r_list = p.findall(html)
        self.write_to_mysql(r_list)

    # 写入csv文件
    # def write_file(self, r_lsit):
    #     with open(self.filename, 'a', newline='') as f:
    #         write_csv = csv.writer(f)
    #         if not self.page:
    #             write_csv.writerow(["小区", "户型", "面积", "装修情况", "总价", "单价"])
    #         for data in r_lsit:
    #             write_csv.writerow(data)

    def write_to_mysql(self, r_list):
        with self.db.cursor() as cur:
            # 处理mysql中的warning
            warnings.filterwarnings("ignore")
            try:
                cur.execute("CREATE DATABASE IF NOT EXISTS SpiderDB")
                cur.execute("USE SpiderDB")
                cur.execute(
                    "CREATE TABLE if not exists lianjia_ersou(ID INT primary key auto_increment,h_name varchar(50),"
                    "h_type varchar(20),h_size varchar(20),h_decr varchar(20),h_price int,h_sPrice int)")
            except Warning:
                pass

            ins = "insert into lianjia_ersou(h_name,h_type,h_size,h_decr,h_price,h_sPrice)" \
                  " values(%s,%s,%s,%s,%s,%s)"
            # 批量写入
            cur.executemany(ins, r_list)
            # 注意一定要提交
            self.db.commit()

    # 主函数
    def main(self):
        total_page = int(input("请输入爬取的页数(最多可输入100):"))
        for i in range(1, total_page + 1):
            print(f'正在爬取第{i}页/共{total_page}页....')
            url = self.base_url + str(i)
            try:
                self.get_page(url)
                self.page += 1
            except Exception:
                print(f"可能被反爬了,程序已终止", "程序已爬取了{self.page}页数据")
                return

            # 爬取成功后随机休息2-5秒
            time.sleep(random.randint(2,5))
        print('爬取成功...')


if __name__ == "__main__":
    spider = LianjiaSpider()
    spider.main()
