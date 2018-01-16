import os
"""
     spider.py爬取后保存的favorite.csv文件里每行末尾都多了一个换行符
     导致打开Excel后发现信息是隔行存储的，也就是每行商品信息的下一行是空行，然后再是商品信息
     我查了半天，干脆写个函数来删除多余的空白行
     请给下面的count变量赋值为你所爬取数据的条数
"""
count = 127


# 读取原文件，隔行写入新文件，最后删除原文件
def delete_line_break():
    with open('favorite.csv', 'r') as f:
        for i in range(count * 2):
            a = f.readline()
            f.readline()
            with open('favorite_books.csv', 'a') as q:
                q.write(a)
    # 删除原文件
    os.remove('favorite.csv')
    print('改写文件成功！')


if __name__ == '__main__':
    delete_line_break()