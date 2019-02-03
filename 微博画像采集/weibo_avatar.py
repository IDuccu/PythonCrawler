"""
    此程序为一个微博画像采集工具
"""
import json
import time

import numpy
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba.analyse
from PIL import Image, ImageSequence
from html2text import html2text
import requests


# 获取uid的用户信息
def get_user_info(uid):
    result = requests.get(f'https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}')
    json_data = result.json()['data']
    userinfo = {
        'name': json_data['userInfo']['screen_name'],
        'description': json_data['userInfo']['description'],
        'follow_count': json_data['userInfo']['follow_count'],
        'followers_count': json_data['userInfo']['followers_count'],
        'profile_image_url': json_data['userInfo']['profile_image_url'],
        'verified_reason': json_data['userInfo']['verified_reason'],
        'containerid': json_data['tabsInfo']['tabs'][1]['containerid'],
    }
    if json_data['userInfo']['gender'] == 'm':
        gender = '男'
    elif json_data['userInfo']['gender'] == 'f':
        gender = '女'
    else:
        gender = '未知'
    userinfo['gender'] = gender
    return userinfo


# 获取古力娜扎的信息
# userinfo = get_user_info('1350995007')
# print(userinfo)

# 循环获取containerid的所有博文
def get_all_post(uid, containerid):
    page = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # 此变量用于存放博文
    blog_text = []
    while 1:
        result = requests.get(f'https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}&containerid={containerid}&page={page}', headers=headers)
        if result.status_code == 200:
            json_data = result.json()
            json_data = json_data.get('data', None)
            # 博文获取完毕则退出循环
            if not json_data['cards']:
                print("爬取完毕正在写入文件...")
                break
            for i in json_data['cards']:
                if i.get('mblog', {}).get('text', {}):
                    blog_text.append(i['mblog'].get('text'))
        # 每次停顿0.5秒 避免被反爬
        time.sleep(0.5)
        page += 1
    return blog_text


# 将爬取的数据写入文件
def write_to_file(userinfo, blog_text):
    filename = userinfo.get('name') + '.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(userinfo)+'\n')
        for i in blog_text:
            f.write(i+'\n')


# 流程控制
def clawer_control():
    uid = input('请输入用户uid:')
    userinfo = get_user_info(uid)
    blog_text = get_all_post(uid, userinfo['containerid'])
    content = '\n'.join([html2text(i) for i in blog_text])
    # 使用jieba的textrank提取出1000个关键字及其比重
    result = jieba.analyse.textrank(content, topK=1000, withWeight=True)

    # 生成关键词比重词典
    keywords = dict()
    for i in result:
        keywords[i[0]] = i[1]

    # 生成词云图
    image = Image.open('./static/images/personas.png')
    graph = numpy.array(image)

    # 生成云图, 注意WordCloud 默认不支持中文,故需导入字库
    wc = WordCloud(font_path='./fonts/yahei.ttf', background_color='white', max_words=300, mask=graph)
    wc.generate_from_frequencies(keywords)
    image_color = ImageColorGenerator(graph)

    # 显示图片
    plt.imshow(wc)
    plt.imshow(wc.recolor(color_func=image_color))
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    clawer_control()
