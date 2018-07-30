# Lagou_mutilprocessing
采用多进程的方法爬取拉勾网职位

### 环境需求

1. python3.5+
2. requests
3. BeautifulSoup
4. hashlib
5. lxml
6. pymongo

### 操作方式

1. 运行channel.py，获取拉勾网首页大类的网址
2. counts.py可以用来查看爬取的数量，如想计数，请先运行此文件后在运行主文件
3. 在终端输入指令 python main.py,开启多线程。

###tips:

1. lagou.py中爬取的是列表页的职位信息，具体页的职位信息爬取附在最后，如需爬取，请自行开启，并在main.py中进行相关的设置的改变。
