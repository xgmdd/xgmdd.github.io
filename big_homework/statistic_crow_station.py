# -*- coding: utf-8 -*-
"""
@author: Issac
"""
'''统计拥挤程度占比随不同车站的变化'''
import pandas as pd
import numpy as np
from processdata import get_total_times
dic = {'#79be85':'green','#ecce39':'yellow','#de7009':'orange','#f20a0a':'red'} # or black（red）
def get_total(day:int):
    """获得第day天拥挤程度随不同车站的统计表"""
    f=pd.read_csv('./output/tables/station-p/day4/page_1.csv',encoding='utf-8')
    # print(f['name'])
    # print('苹果园' in f['name'])
    of=pd.DataFrame(np.zeros([len(f['name']),4]),index=f['name'],dtype=int,columns=['green','yellow','orange','red'])
    # print(of)
    # print(of['green']['苹果园'])
    for i in range(get_total_times(day)):
        df=pd.read_csv('./output/tables/station-p/day{}/page_{}.csv'.format(day,i),encoding='utf-8')
        
        for line in df.itertuples():
            # print("line"+str(line))
            of[dic[line.color]][line.name]=of[dic[line.color]][line.name]+1
        print(i)
    of.to_csv('./tmp/total.csv')
    print("file total.csv generated")

from pyecharts import options as opts
from pyecharts.charts import Bar,Tab
from pyecharts.commons.utils import JsCode
def calc_day(day:int):
    get_total(day)

    # 绘制表格


    f=pd.read_csv('./tmp/total.csv',encoding='utf-8')
    lists=f['name']
    #print(list(lists))
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    tt=get_total_times(day)
    for i in range(0,394):
        list2.append({"value":int(f['green'][i]),"percent":f['green'][i]/tt})
        list3.append({"value":int(f['yellow'][i]),"percent":f['yellow'][i]/tt})
        list4.append({"value":int(f['orange'][i]),"percent":f['orange'][i]/tt})
        list5.append({"value":int(f['red'][i]),"percent":f['red'][i]/tt})
    c1 = (
    Bar(init_opts=opts.InitOpts())
    .add_xaxis(list(lists))
    .add_yaxis("green", list2, stack="stack1", category_gap="0%",color='green')
    .add_yaxis("yellow", list3, stack="stack1", category_gap="0%",color='yellow')
    .add_yaxis("orange", list4, stack="stack1", category_gap="0%",color='orange')
    .add_yaxis("red", list5, stack="stack1", category_gap="00%",color='red')
    .set_series_opts(
        label_opts=opts.LabelOpts(
            position="right",
            formatter=JsCode(
                "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
            ),
        )
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
        datazoom_opts=[opts.DataZoomOpts()],
        title_opts=opts.TitleOpts(title="station crowd percentage")
    )
    #.render("./charts/station_bar_percent.html")
    )
    return c1
ta=Tab()

for i in range(6):
    ta.add(calc_day(i),'day{}'.format(i))
ta.render("./charts/station_bar_percent.html")