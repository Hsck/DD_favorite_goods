简介
===
借用selenium + Chrome，在程序休眠时间手动登陆当当网，构建session并保存cookies信息后关闭页面<br/>
分析Ajax，session.get()请求URL，解码JSON格式的数据并解析，最后把数据写入CSV文件

注意
---
写入的CSV文件格式有点不对，请运行Delete_extra_lines.py来删除多余空行

爬取效果图
---
![](https://github.com/Hsck/DD_favorite_goods/raw/master/img/1.jpg)
