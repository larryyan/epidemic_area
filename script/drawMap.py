from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

def main():
    dangerLocation = [l.split('\n')[0] for l in open("location.txt", "r").readlines()]

    # 链式调用
    c = Geo().add_schema(maptype="北京")
    for i in range(len(dangerLocation)):
        name, a, b = dangerLocation[i].split(' ')
        # 加入自定义的点，格式为
        c.add_coordinate(name, a, b) 
        # 为自定义的点添加属性
        c.add("病例", [(name, 1)])
    c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    c.set_global_opts(title_opts=opts.TitleOpts(title="北京昨日新增疫情地图"))
    # 在 html(浏览器) 中渲染图表
    c.render()

main()