# 北京新增疫情地图
- 北京各区疫情发布信息繁杂，本项目数据来源当日《北京日报》信息爬取

## 介绍

- python爬虫爬取《北京日报》新闻
- 通过高德地图api搜索目标地址的经纬度
- 通过pyecharts构建地图

## 使用方式

- 安装requirements.txt中的依赖
- 创建key.txt 输入自己的高德地图key（前往[高德开放平台](https://console.amap.com/dev/key/app)申请）
- 运行

```shell
python3 map.py
```

- 打开render.html即可查看地图

