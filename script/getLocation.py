# -*- coding: utf-8 -*-
import json  # 解析json数据
import urllib.request  # 发送请求
from urllib import parse  # URL编码

class Info:
    def __init__(self, mykey, city, keywords):
        self.mykey = mykey
        self.city = city
        self.keywords = keywords
        self.types = ""
 
def getGDLocation(input):
    ans = []
    parameters = "key={}&keywords={}&types={}&city={}&children=0&offset=&page={}&extensions=all" \
        .format(input.mykey, input.keywords, input.types, input.city, 1)  # 参数
    url = "https://restapi.amap.com/v3/place/text?{}".format(parameters)  # 拼接请求
    newUrl = parse.quote(url, safe="/:=&?#+!$,;'@()*[]")  # 编码
    response = urllib.request.urlopen(newUrl)  # 发送请求
    data = response.read()  # 接收数据
    jsonData = json.loads(data)  # 解析json文件
    for i in range(len(jsonData['pois'])):
        num_location = jsonData['pois'][i]['location']
        ans.append(num_location)

    if not ans:
        input.keywords = input.keywords[input.keywords.find("区") + 1:]
        ans = getGDLocation(input)
    return ans

def main():
    dangerPlace = [l.split('\n')[0] for l in open("data/location.txt", "r", encoding='utf-8').readlines()]
    
    dangerPlaceLocation = {}
    try:
        key = open('key.txt','r').readlines()[0]
        for item in dangerPlace:
            info = Info(key, "北京", item)
            x, y = getGDLocation(info)[0].split(',')
            dangerPlaceLocation.update({item: [x, y]})
    except Exception as e:
        print("无法正常读取key.txt", e)
    
    with open("data/location.txt","w", encoding='utf-8') as file:
        for item in dangerPlaceLocation:
            loc = dangerPlaceLocation[item]
            file.writelines(item+' '+loc[0]+' '+loc[1]+'\n')
