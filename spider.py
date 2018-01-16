import csv
import json
from json import JSONDecodeError
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://myhome.dangdang.com/myFavorite',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
}

chrome = webdriver.Chrome()
session = requests.Session()    # 构建session
count = 0             # 写入数据的行计数器
final_data = []       # 列表存储爬取的所有收藏商品信息


def login():
    """
        偷懒式模拟登陆当当网：
        使用selenium打开登陆界面，在程序休眠的时间内手动填写账号密码登陆或是扫码登陆，
        登陆后程序会获取cookies信息并保存
    """
    try:
        login_url = 'https://login.dangdang.com/signin.aspx?returnurl=http%3A//www.dangdang.com/'
        chrome.get(login_url)
        # 程序休眠时间
        time.sleep(30)
        cookies = chrome.get_cookies()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
    except TimeoutException:
        login()
    finally:
        chrome.close()


# session请求页面url,返回页面text信息
def get_page(url):
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        print(response.status_code)
    except Exception:
        print('请求页面异常！', url)
        pass


def parse_page(text):
    """
        解码json格式的数据(text)，迭代提取出收藏商品信息，
        当字典data的键'errorCode'的值为404时，即信息为空时，
        调用write_to_csv()函数将信息写入csv文件，最后结束程序
    """
    try:
        # 解码json数据
        data = json.loads(text)
        if data.get('errorCode') == 200 and 'info' in data.keys():
            for product in data.get('info').get('list'):
                yield [
                    product.get('product_id'),            # 商品ID
                    product.get('product_name'),          # 商品名称
                    product.get('show_price'),            # 商品价格
                    product.get('product_image'),         # 商品图片
                    product.get('product_comment'),       # 评论数量
                    product.get('favorie_num')            # 收藏数量
                ]
        elif data.get('errorCode') == 404:
            print('商品收藏数据为空,结束爬虫')
            print('共计爬取 %d 条数据' % count)
            # 调用函数，将爬取到的所有数据写入CSV文件
            write_to_csv()
            # 结束程序
            exit()
        else:
            print('商品收藏信息出错，请检查数据')
            print(data)
    except JSONDecodeError:
        print('JSON解码异常!')
    except Exception:
        print('解析商品收藏信息异常!')


def write_to_csv():
    with open('favorite.csv', 'w+') as f:
        writer = csv.writer(f, dialect='excel')
        # 写入标题行
        writer.writerow(["商品ID", "商品名称", "商品价格", "商品图片", "评论数量", "收藏数量"])
        # 将final_data中的数据循环写入到CSV文件中
        for item in final_data:
            writer.writerow(item)
    print('写入到csv文件成功！')


def main(page):
    url = 'http://myhome.dangdang.com/myFavoriteInfo?type=1&page_index=' + str(page)
    print('爬取第 %d 页商品收藏' % page)
    text = get_page(url)
    for info in parse_page(text):
        final_data.append(info)
        global count
        count += 1
    time.sleep(1)


if __name__ == '__main__':
    login()      # 手动模拟登陆
    session.headers.clear()
    for i in range(1, 100):
        main(i)
