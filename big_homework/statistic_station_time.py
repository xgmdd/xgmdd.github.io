# -*- coding: utf-8 -*-
"""
@author: Issac
"""
'''由已有数据获得车站拥挤度空间分布随时间的变化数据并绘制地图'''

import pandas as pd
# 颜色代码常量转换
dic = {'green':'#79be85','yellow':'#ecce39','orange':'#de7009','red':'#f20a0a'} # or black（red）


def get_crowd(color:str,j:int,i:int):
    """获得j天i次爬取所有为color的车站名称和这次的爬取时间"""
    df = pd.read_csv('./output/tables/station/day{}/page_{}.csv'.format(j,i)) # 读取csv文件
    
    names= df[df['color'] == dic[color]]['name'] # 选取第二列为color的行，选取第一列的元素并转换为列表
    # 打开经纬度坐标信息表
    df=pd.read_csv('./data/position.csv',encoding='utf-8',delimiter='\t')
    # 准备写临时json
    file= open('./tmp/station_{}.json'.format(color),'w',encoding='utf-8')
    file.write('{\n')
    flag=True
    # 将站名经纬度写入json
    np=[]
    for name in names:
        f2=True
        for d in df[df['b']==name]['d']:
            for e in df[df['b']==name]['e']:
                # print(name,d,e)
                f2=False
                if flag:
                    file.write('"' + name + '":[' + str(d) + ',' + str(e)+']')
                    flag=False
                else:
                    file.write(',\n"' + name + '":[' + str(d) + ',' + str(e)+']')
        if not f2:
            np.append(name)
    file.write('\n}')
    file.close()
    #print("done"+color)
    # 返回爬取时间
    f=pd.read_csv('./output/tables/number_time/day{}.csv'.format(j))
    # print(f)
    t=f['time'][i]
    return np,t


from processdata import get_total_times



from pyecharts import options as opts
from pyecharts.charts import Geo, Timeline
from pyecharts.faker import Faker
from pyecharts.globals import ChartType, SymbolType, GeoType

tl = Timeline()
tl.page_title="周一地铁站拥挤情况变化"
for i in range(get_total_times(4)):
    n,t=get_crowd('yellow',4,i)
    n2,t=get_crowd('orange',4,i)
    n3,t=get_crowd('red',4,i)
    map0 = (
        Geo()
        .add_coordinate_json(json_file='./tmp/station_yellow.json')
        .add_coordinate_json(json_file='./tmp/station_orange.json')
        .add_coordinate_json(json_file='./tmp/station_red.json')
        .add_schema(maptype="北京")
        .add("yellow",
            zip(n,n),
            type_=ChartType.EFFECT_SCATTER,
            color='yellow',
            label_opts=opts.LabelOpts(is_show=False,)
        )  
        .add("orange",
            zip(n2,n2),
            type_=ChartType.EFFECT_SCATTER,
            color='orange',
            label_opts=opts.LabelOpts(is_show=False,)
        )  
        .add("red",
            zip(n3,n3),
            type_=ChartType.EFFECT_SCATTER,
            color='red',
            label_opts=opts.LabelOpts(is_show=False,)
        ) 
    )
    tl.add(map0, "{}".format(t))
    print("done"+str(i))
tl.render("./charts/timeline_map.html")


