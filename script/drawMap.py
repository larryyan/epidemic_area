from pyecharts import options as opts
from pyecharts.charts import Geo


def main():
    dangerLocation = [l.split('\n')[0] for l in open("data/location.txt", "r").readlines()]
    patientNum = [l.split('\n')[0] for l in open("data/number.txt", "r").readlines()]   

    maps = Geo().add_schema(maptype="北京")
    for i in range(len(dangerLocation)):
        name, a, b = dangerLocation[i].split(' ')
        num = int(patientNum[i])

        maps.add_coordinate(name, a, b)
        maps.add("病例", [(name, num)])
    maps.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    maps.set_global_opts(title_opts=opts.TitleOpts(title="北京昨日新增疫情地图"))
    
    maps.render()
