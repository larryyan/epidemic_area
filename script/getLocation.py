# -*- coding: utf-8 -*-
import json  # 解析json数据
import urllib.request  # 发送请求
from math import ceil
from urllib import parse  # URL编码

class Info:
    def __init__(self, mykey, city, keywords):
        self.mykey = mykey
        self.city = city
        self.keywords = keywords
        self.types = ""
 
def getGDLocation(input):
 
    def get_page():
        parameters = "key={}&keywords={}&types={}&city={}&children=0&offset=&page=1&extensions=all" \
            .format(input.mykey, input.keywords, input.types, input.city)  # 参数
        url = "https://restapi.amap.com/v3/place/text?{}".format(parameters)  # 拼接请求
        newUrl = parse.quote(url, safe="/:=&?#+!$,;'@()*[]")  # 编码
        response = urllib.request.urlopen(newUrl)  # 发送请求
        data = response.read()  # 接收数据
        jsonData = json.loads(data)  # 解析json文件
        page = eval(jsonData['count'])
        return page
 
    def get_json(page):
        parameters = "key={}&keywords={}&types={}&city={}&children=0&offset=&page={}&extensions=all" \
            .format(input.mykey, input.keywords, input.types, input.city, page)  # 参数
        url = "https://restapi.amap.com/v3/place/text?{}".format(parameters)  # 拼接请求
        newUrl = parse.quote(url, safe="/:=&?#+!$,;'@()*[]")  # 编码
        response = urllib.request.urlopen(newUrl)  # 发送请求
        data = response.read()  # 接收数据
        jsonData = json.loads(data)  # 解析json文件
        return jsonData
 
    # 写入数据入字典
    page = ceil(get_page() / 20)
    ans = []
    for i in range(1, page + 1):
        jsonData = get_json(i)
        for i in range(len(jsonData['pois'])):
            # name = jsonData['pois'][i]['name']
            num_location = jsonData['pois'][i]['location']
            ans.append(num_location)
    return ans

def main():
    dangerPlace = [l.split('\n')[0] for l in open("data.txt", "r").readlines()]
    
    dangerPlaceLocation = {}
    key = open('key.txt','r').readlines()[0]
    # print(key)
    for item in dangerPlace:
        info = Info(key, "北京", item)
        x, y = getGDLocation(info)[0].split(',')
        print(x, ' ', y)
        dangerPlaceLocation.update({item: [x, y]})
    
    # print(dangerPlaceLocation)
    with open("location.txt","w") as file:
        for item in dangerPlaceLocation:
            loc = dangerPlaceLocation[item]
            file.writelines(item+' '+loc[0]+' '+loc[1]+'\n')

# main()
    

'''
# 读取
from openpyxl import load_workbook
wb2 = load_workbook('position.xlsx')
'''

