import json
import re
import threading
import time
from queue import Queue

import requests
import random


URL = "https://www.neihan8.com/wenzi/index_%s.html"


# 此函数读取文件并返回一个ua池列表
def get_ua(filename):
    with open(filename, "r", encoding="utf-8") as uaf:
        ua_list = [ua.strip() for ua in uaf if ua.strip()]
    return ua_list


def get_one_page(url, ua=None, retries=5, max_s=2):
    if not retries:
        with open("error.txt", 'a', encoding='utf-8') as erf:
            erf.write(f"serverErrorCode:{response.status_code}    url:{url}\n")
        return None
    if ua:
        headers = {
            "Connection": "keep-alive",
            "User-Agent": ua,
            "Host": "www.neihan8.com"
        }
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url)
    response.encoding = "utf-8"
    if response.status_code == 200:
        return response.text
    elif 500 <= response.status_code < 600:
        time.sleep(max_s)
        get_one_page(url, ua, retries-1, max_s*2)
    else:
        with open("error.txt", 'a', encoding='utf-8') as erf:
            erf.write(f"ErrorCode:{response.status_code}   url:{url}\n")
        return None


def parse_one_page(html):
    pattern = re.compile(r'<div class="text-column-item box box-790">'
                         r'[\s\S]*?<a href="([\s\S]*?)" class="title" title="([\s\S]*?)">')
    items = re.findall(pattern, html)
    for it in items:
        yield {it[0].strip(): it[1].strip()}


def write_to_file(dic):
    with open("内涵段子.txt", 'a', encoding="utf-8") as wtf:
        wtf.write(json.dumps(dic, ensure_ascii=False)+"\n")


def craw_contral(url, ua):
    """获取请求对象"""
    lock.acquire()
    try:
        time.sleep(random.randint(1, 3))
        html = get_one_page(url, ua)
        if html:
            item = parse_one_page(html)
            for it in item:
                write_to_file(it)
    except Exception as e:
        print(e, '\n')
        print(url)
    lock.release()


if __name__ == "__main__":
    ua_list = get_ua("user_agent.txt")
    # 创建一个消息队列对象
    q = Queue()
    # 构造url_list列表
    url_list = ["https://www.neihan8.com/wenzi/index.html"]
               + [(URL %i) for i in range(2,202)]
    # 创建一个线程列表
    thread_list = []
    lock = threading.Lock()
    for url in url_list:
        random.shuffle(ua_list)
        t = threading.Thread(target=craw_contral, args=(url, ua_list[0]))
        t.start()
        thread_list.append(t)
    for i in thread_list:
        i.join()







