import warnings

warnings.filterwarnings("ignore")
from urllib import request
from bs4 import BeautifulSoup as bs
import gzip


# 分析首页函数
def getWeb():
    # 防止被网站禁用爬虫，增加headers
    # USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    HEADERS = {

        "User-Agent": USER_AGENT

    }
    url = 'https://www.takefoto.cn'
    resp = request.Request(url, headers=HEADERS)
    resp = request.urlopen(resp)
    html_data = resp.read().decode('utf-8')
    soup = bs(html_data, 'html.parser')
    newsListDiv = soup.find_all('div', class_='banner')
    newsList = newsListDiv[0].find_all('li', class_=None)
    for item in newsList:
        newsList_a = item.find_all('a', target='_blank')
        for i in newsList_a:
            if i.text.find('北京昨日新增')==-1:
                continue
            neturl = i['href']
            return neturl
    
    return None


# 爬取患者函数
def getPatientList(url):  # 参数为url

    requrl = url
    print(requrl)
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
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
    article_text = soup.find_all('div', class_='article-text')
    patientList_p = article_text[0].find_all('p')

    patientList = []

    for item in patientList_p:
        if item.text.find('现住')==-1 or (item.text.find('确诊病例')==-1 and item.text.find('无症状感染者')==-1):
            continue
        patientList.append(item.text)

    return patientList


def main():
    # newsWeb = getWeb()
    newsWeb = '//www.takefoto.cn/news/2022/05/15/10087493.shtml'
    print(newsWeb)
    PatientList = getPatientList('https:'+newsWeb)
    
    dangerPlace = []
    for item in PatientList:
        beg = item.find('现住')+2
        end = item.find('。')
        print(item[beg:end])
        dangerPlace.append(item[beg:end])
    with open("data.txt","w") as f:
        for item in dangerPlace:
            f.writelines(item+'\n')


# 主函数
# main()
