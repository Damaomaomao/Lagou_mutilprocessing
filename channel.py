from  bs4 import BeautifulSoup
import requests
import pymongo


#--------<<链接mongoDB>>-----------
client = pymongo.MongoClient(host="localhost")
lagou = client['lagou']
channel = lagou['channel']

#-----------<<获取首页大类网址>>----------------------
start_url = "https://www.lagou.com/"
host = "www.lagou.com"

headers = {
    'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Cookies": "user_trace_token=20180415174704-1ec6ac99-aaf2-4748-9f35-df8ca538b590; _ga=GA1.2.1884902336.1523785624; LGUID=20180415174704-f4692dd4-4091-11e8-862c-525400f775ce; LG_LOGIN_USER_ID=cacc114600e6ad784d06c04e01736c1911194b7615d77055a86f492c20a56d80; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.1245467970.1532349094; WEBTJ-ID=20180724100742-164ca0aca6c6d-085d3ce40572be-6114147a-2073600-164ca0aca6d38b; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1529972253,1532349094,1532351938,1532398062; LGSID=20180724100951-a637f8de-8ee6-11e8-9ee6-5254005c3644; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rsv_spt%3D1%26rsv_iqid%3D0xf165cf0e00057e46%26issp%3D1%26f%3D3%26rsv_bp%3D0%26rsv_idx%3D2%26ie%3Dutf-8%26tn%3Dbaiduhome_pg%26rsv_enter%3D1%26rsv_sug3%3D7%26rsv_sug1%3D7%26rsv_sug7%3D100%26rsv_sug2%3D1%26prefixsug%3D%2525E6%25258B%252589%2525E9%252592%2525A9%26rsp%3D0%26inputT%3D5082%26rsv_sug4%3D5083; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_baidu_pc; X_HTTP_TOKEN=3561738c424bbb43349c44577002b47b; _putrc=50EDE64BCF01A97C123F89F2B170EADC; JSESSIONID=ABAAABAAAIAACBI4EFDD9A98DABB96CA4E0D2E5D64C27D8; login=true; unick=%E6%AF%9B%E4%BD%B3%E8%BF%AA; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; gate_login_token=4dd04f478cfec90cfd15337a379ad58c22e0f97a3ba466fb1e839ef257d164b3; _gat=1; TG-TRACK-CODE=index_recjob; LGRID=20180724101606-85c2de8a-8ee7-11e8-a385-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532398438; X_MIDDLE_TOKEN=f2f8d91c94e2be546bbbbe95b19e322e",

}
def parse_index(url):
    web_data = requests.get(url,headers = headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    all_positions = soup.select('div.menu_sub.dn > dl > dd > a')
    joburls = [i['href'] for i in all_positions]
    jobnames = [i.get_text() for i in all_positions]
    
    for joburl,jobname in zip(joburls,jobnames):
        data={
               "url":joburl,
               "jobname":jobname,
                }
        channel.insert_one(data)
        
if __name__ == '__main__':
    parse_index(start_url)





