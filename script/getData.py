from cgitb import text
import warnings

warnings.filterwarnings("ignore")
from urllib import request
from bs4 import BeautifulSoup as bs
import gzip
import json
import re


# 分析首页函数
def getWeb():
    # 防止被网站禁用爬虫，增加headers
    # USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    HEADERS = {

        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "s.bjd.com.cn",
        "sec-ch-ua": '''" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"''',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"

    }
    url = 'https://s.bjd.com.cn/api/search/get?page=1&keyboard=%E5%8C%97%E4%BA%AC%E6%98%A8%E6%97%A5%E6%96%B0%E5%A2%9E&sort=publishTime'
    resp = request.Request(url, headers=HEADERS)
    resp = request.urlopen(resp)
    json_data = json.loads(resp.read())['data']['data']

    for item in json_data:
        if item['catname'] != '首都':
            continue
        title = item['title']
        if title.find('一图速览')!=-1:
            continue
        return item['title_url']

    return None

def getPatientNumber(string):
    end = string.find('：')
    def num(text):
        dunhao = text.find('、')
        if dunhao == -1:
            num_list = re.findall(r"\d+", text)
            if len(num_list) == 1:
                return 1
            else:
                return int(num_list[1]) - int(num_list[0])
        number = num(text[dunhao+1:])
        num_list = re.findall(r"\d+", text[:dunhao])
        if len(num_list) == 1:
            return 1 + number
        else:
            return int(num_list[1]) - int(num_list[0]) + number
    return num(string[:end])

# 爬取患者函数
def getPatientList(url):  # 参数为url

    requrl = url
    print(requrl)
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
    HEADERS = {

        "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        "User-Agent": USER_AGENT,
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }
    resp = request.Request(requrl, headers=HEADERS)
    resp = request.urlopen(resp)
    html_data = gzip.decompress(resp.read()).decode('utf-8')
    soup = bs(html_data, 'html.parser')
    article_text = soup.find_all('div', class_='bjd-article-centent')
    patientList_p = article_text[0].find_all('p')

    patientDict = {}

    for item in patientList_p:
        if item.text.find('现住')==-1 or (item.text.find('确诊病例')==-1 and item.text.find('感染者')==-1):
            continue
        beg = item.text.find('现住')+2
        end = item.text.find('。', beg)
        if item.text.find('，', beg)!=-1:
            end = min(end, item.text.find('，', beg))
        if item.text.find('位于', 0, end)!=-1:
            beg = max(beg, item.text.find('位于', 0, end)+2)
        dangerPlace = item.text[beg:end]
        current_patient_number = patientDict.get(dangerPlace, 0)
        patientDict[dangerPlace] = getPatientNumber(item.text) + current_patient_number

    return patientDict


def main():
    newsWeb = getWeb()
    # newsWeb = '//www.takefoto.cn/news/2022/05/15/10087493.shtml'
    print(newsWeb)

    PatientDict = getPatientList('https:'+newsWeb)
    
    with open("data/data.txt","w") as f1:
        for item in PatientDict.keys():
            f1.writelines(item+'\n')
    
    with open("data/number.txt","w") as f2:
        for item in PatientDict.values():
            f2.writelines(str(item)+'\n')


# 主函数
# main()
