"""
-- 抓取百度贴吧里帖子里的所有图片
例如: 输入校花吧
    会爬取所有校花吧内所有帖子的图片
    进入每一个帖子,然后抓取帖子里的图片
    1.思路
        1.找到贴吧主页的url,下一页: 找规律
            http://tieba.baidu.com/f?kw=校花&png=0
            http://tieba.baidu.com/f?kw=校花&pn=50
        2.获取一页中每个帖子的url
        3.对每个url发请求,获取帖子里图片url
        4.对图片url发请求,以wb的方式写入本地文件
    2.步骤
        1.获取贴吧主页的url
            http://tieba.baidu.com/f?kw={查询参数}&png=0
        2.找到页面中所有帖子的url -- 使用xpath
            //div[@class="threadlist_lz clearfix"]//a/@href
            帖子的url为 http:tieba.baidu.com/ + 匹配到的相对url
        3.找每个帖子的图片的url -- xpath匹配
            //img[@class="BDE_Image"]/@src  #返回的是绝对地址,不用拼接
        4.代码实现
"""
import os
import time
from random import randint

import requests
from lxml import etree


# ==========================================================
# 注意使用xpath时一定要注意!!!! 不同浏览器可能会返回不同的页面,
# 可能导致匹配不到结果,建议使用IE作为User-Agent
# ==========================================================
class TiebaImgSpider:
    def __init__(self):
        self.base_url = "http://tieba.baidu.com/f?"
        self.base_url_tieba = "http://tieba.baidu.com"
        self.headers = {
            'User-Agent': "Mozilla/5.0"}
        self.name = input("请输入贴吧名称:")
        # 定义爬取的页数
        self.page = 0
        # 每条帖子的相对url的xpath表达式
        self.xp1 = '//div[@class="t_con cleafix"]/div/div/div/a/@href'
        # 每条帖子图片的url的xpath表达
        self.xp2 = r'//img[@class="BDE_Image"]/@src'
        # 记录图片的个数
        self.pn = 1

    def get_page(self, url, params=None):
        res = requests.get(url, headers=self.headers, params=params)
        res.encoding = 'utf-8'
        html = res.text
        return html

    def parse_page(self, xp, html):
        # 创建解析对象
        parse_html = etree.HTML(html)
        r_list = parse_html.xpath(xp)
        return r_list

    def write_img(self, url):
        res = requests.get(url, self.headers)
        data = res.content
        # 将图片写入文件
        with open(f"{self.name}\\{self.name}_{self.pn}.jpg", 'wb') as f:
            print(f"正在写入: {self.name}_{self.pn}.jpg")
            f.write(data)
            time.sleep(randint(1, 3))
            self.pn += 1

    def work_on(self):
        # 创建一个文件夹保存数据
        if not os.path.exists(f'{self.name}'):
            os.mkdir(f"{self.name}")
        # 爬取页数
        num = int(input("请输入爬取页数:"))
        for i in range(num):
            print(f"***********正在爬取第{i + 1}页******************")
            # 构造参数
            params = {"kw": self.name,
                      "pn": i * 50,
                      }
            page_html = self.get_page(self.base_url, params=params)
            # 每条帖子的相对url列表
            stick_list = self.parse_page(self.xp1, page_html)
            # 每页进度计数
            count = 1
            # 帖子的绝对url
            for url in stick_list:
                stick_url = self.base_url_tieba + url
                stick_html = self.get_page(stick_url)
                # 解析每条帖子中的图片url
                img_list = self.parse_page(self.xp2, stick_html)
                for i_url in img_list:
                    self.write_img(i_url)
                print(f'-----本页已完成 {count / len(stick_list) * 100} %-----')
                count += 1
            print(f"+++++++第{i + 1}页/共{num}页,爬取完毕,总进度( {(i+1) / num * 100} %)++++++")
            self.page += 1
        print(f"共计写入了{self.pn}张图片")


if __name__ == "__main__":
    spider = TiebaImgSpider()
    spider.work_on()
