# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 19:38:11 2018

@author: Administrator
"""
from multiprocessing import Pool
import pymongo
from lagou import get_info , parse_info
import random
import time

client = pymongo.MongoClient(host="localhost")
lagou = client['lagou']
channel = lagou['channel']
lagoujob = lagou['lagoujob']
lgjob = lagou["lgjob"]

channel_list = [item['url'] for item in channel.find()]
link_list = [item['link'] for item in lgjob.find()]
time_snap = random.randint(0,8)


def get_all_links_from(channel):
    for page in range(1,30):
        get_info(channel,page)
        time.sleep(time_snap)

#--------<<列表页简单信息抓取>>-------------------
if __name__ == '__main__':
    t_start = time.time()

    pool = Pool(processes=4)
    pool.map(get_all_links_from,channel_list)

    print(time.time() - t_start)



#-----------------<<具体页信息抓取>>------------
# if __name__ == '__main__':
#     t_start = time.time()
#
#     pool =Pool(processes=6)
#     pool.map(parse_info,link_list)
#
#     print(time.time() - t_start)
#
