# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 11:18:48 2018

@author: Administrator
"""

import requests
import hashlib
import random
from lxml import etree
import pymongo
import time
import random
# import datetime
# import re
# from requests import RequestException


client = pymongo.MongoClient(host="localhost")
lagou = client['lagou']
channel = lagou['channel']
lagoujob = lagou['lagoujob']
lgjob = lagou["lgjob"]
url_list = lagou['url_list']

#请登陆后进行填充该信息，建议多用几个浏览器的信息
header_list= [{'User-Agent':"",
           "Cookie":""},
{'User-Agent':"",
 "Cookie":"",}]


def get_md5(url):
    if isinstance(url,str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

#=================================<<获取列表页的信息>>======================================
def get_info(channel,page):
    url = '{}{}/?filterOption={}'.format(channel,str(page),str(page))
    response = requests.get(url,headers = random.choice(header_list)).text
    bug = "i_error"
    if  bug in response:
        print("访问的页面不存在")
        pass
    else:
        html = etree.HTML(response)
        infos = html.xpath("//ul[@class='item_con_list']/li")       
        for info in infos:
            link = info.xpath("div/div/div/a/@href")[0]
            link_id = get_md5(link)
            position = info.xpath("div/div/div/a/h3/text()")[0]
            addr = info.xpath("div/div/div/a/span[@class='add']/em/text()")[0]
            salary = info.xpath("div/div/div/div/span[@class='money']/text()")[0]
            work_years = "".join(info.xpath("div/div/div/div/text()")[2]).strip().split("/")[0]
            degree_need= "".join(info.xpath("div/div/div/div/text()")[2]).strip().split("/")[1]
            try:
                tag = "/".join(info.xpath("div[2]/div[1]/span/text()"))
            except Exception:
                tag = None   
            company = info.xpath("div[1]/div[3]/a/img/@alt")[0]
            job_advantage = info.xpath("div[2]/div[2]/text()")[0]
            company_field= "".join(info.xpath("div[1]/div[2]/div[2]/text()")[0]).strip().split("/")[0]
            company_stage= "".join(info.xpath("div[1]/div[2]/div[2]/text()")[0]).strip().split("/")[1]
            data = {
                    "link":link,
                    "link_id":link_id,
                    "position":position,
                    "addr":addr,
                    "salary":salary,
                    "work_years":work_years,
                    "degree_need":degree_need,
                    "tag":tag,
                    "company":company,
                    "job_advantage":job_advantage,
                    "company_field":company_field,
                    "company_stage":company_stage,
                    }
            
            save_to_mongodb(data)
            
            

def save_to_mongodb(data):
    try:
        if lgjob.update_one({'link_id': data['link_id']}, {'$set': data}, True):
            print('储存到MONGODB成功',data)
    except:
        print('储存到MONGODB失败',data)
        


# # =========================《获取具体页的信息》====================================================
# def get_one_page(link):
#     try:
#         response = requests.get(link , headers = random.choice(header_list))
#         if response.status_code ==200:
#             if "i_error" in response.text:
#                 pass
#             return response
#         return  None
#     except RequestException:
#         return None

# def get_time(publish_time):
#     match_time1 = re.match("(\d+):(\d+).*", publish_time)
#     match_time2 = re.match("(\d+)天前.*", publish_time)
#     match_time3 = re.match("(\d+)-(\d+)-(\d+)", publish_time)
#     if match_time1:
#         today = datetime.datetime.now()
#         hour = int(match_time1.group(1))
#         minutes = int(match_time1.group(2))
#         time = datetime.datetime(
#             today.year, today.month, today.day, hour, minutes)
#         time_publish= time.strftime("%Y-%m-%d %H:%M:%S")
#     elif match_time2:
#         days_ago = int(match_time2.group(1))
#         today = datetime.datetime.now() - datetime.timedelta(days=days_ago)
#         time_publish = today.strftime("%Y-%m-%d %H:%M:%S")
#     elif match_time3:
#         year = int(match_time3.group(1))
#         month = int(match_time3.group(2))
#         day = int(match_time3.group(3))
#         today = datetime.datetime(year, month, day)
#         time_publish = today.strftime("%Y-%m-%d %H:%M:%S")
#     else:
#         time_publish = datetime.datetime.now(
#         ).strftime("%Y-%m-%d %H:%M:%S")
#     return time_publish

# def parse_info(link):
#     response = get_one_page(link)
#     data = etree.HTML(response.text)
#     title = "".join(data.xpath('//div[@class="job-name"]/@title'))
#     url = response.url
#     url_object_id = get_md5(url)
#     publish_time = data.xpath("//p[@class='publish_time']/text()")
#     if publish_time:
#         publish_time = get_time(publish_time)
#     salary = "".join(data.xpath('//dd[@class="job_request"]/p/span[@class="salary"]/text()'))
#     job_city = "".join(data.xpath("//*[@class='job_request']/p/span[2]/text()")).replace("/","")
#     work_years = "".join(data.xpath("//*[@class='job_request']/p/span[3]/text()")).replace("/","")
#     degree_need = "".join(data.xpath("//*[@class='job_request']/p/span[4]/text()")).replace("/","")
#     job_type = "".join(data.xpath("//*[@class='job_request']/p/span[5]/text()")).replace("/","")
#     job_advantage = "".join(data.xpath("//dd[@class='job-advantage']/p/text()"))
#     job_desc = "".join(data.xpath('//dd[@class="job_bt"]/div/p/text()'))
#     job_addr = "-".join(data.xpath('//div[@class="work_addr"]/a/text()'))[:-4]
#     company_name ="".join(data.xpath('//dl[@class="job_company"]/dt/a/img/@alt'))
#     tags = "/".join(data.xpath('//*[@class="job_request"]/ul/li/text()'))
#     company_url = "".join(data.xpath("//dl[@class='job_company']//a[@rel='nofollow']/@href"))
#     data =  {
#             "title":title,
#             "url":url,
#             "url_object_id":url_object_id,
#             "publish_time":publish_time,
#             "salary":salary,
#             "job_city":job_city,
#             "tags":tags,
#             "work_years":work_years,
#             "degree_need":degree_need,
#             "job_type":job_type,
#             "job_advantage":job_advantage,
#             "job_desc":job_desc,
#             "job_addr":job_addr,
#             "company_name":company_name,
#             "company_url":company_url,
#             }
#     try:
#         if lagoujob.update_one({'link_id': data['link_id']}, {'$set': data}, True):
#             print('储存到MONGODB成功',data)
#     except:
#         print('储存到MONGODB失败',data)
#     time.sleep(random.randint(1,5))
# # =============================================================================
    

        

    
        
    
    
    


            

