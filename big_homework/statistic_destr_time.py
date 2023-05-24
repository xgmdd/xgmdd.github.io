# -*- coding: utf-8 -*-
"""
@author: Issac
"""
'''由已有数据获得车站拥挤度数量分布随时间的变化数据并绘制html表格'''
import pandas as pd
# dic = {'#79be85':'green','#ecce39':'yellow','#de7009':'orange','#f20a0a':'red'} # or black（red）
# 颜色翻译如上
op=['#79be85','#ecce39','#de7009','#f20a0a']
op2=['green','yellow','black']
def get_station_distribution(j:int,i:int):
    '''获得j天i页的车站(绿、黄、橙、红、时间)'''
    f=pd.read_csv('./output/tables/station-p/day{}/page_{}.csv'.format(j,i),dtype=str) 
    cnt=f['color'].value_counts()
    # print(cnt)
    f=pd.read_csv('./output/tables/number_time/day{}.csv'.format(j))
    # print(f)
    t=f['time'][i]
    l=[]
    for c in op :
        if c in cnt.index:
            l.append(int(cnt[c]))
        else:
            l.append(int(0))
    return l,t
def get_segment_distribution(j:int,i:int):
    '''获得j天i页的运行段(绿、黄、红、时间)'''
    f=pd.read_csv('./output/tables/segment-p/day{}/page_{}.csv'.format(j,i),dtype=str) 
    cnt=f['color'].value_counts()
    # print(cnt)
    f=pd.read_csv('./output/tables/number_time/day{}.csv'.format(j))
    # print(f)
    t=f['time'][i]
    l=[]
    for c in op2 :
        if c in cnt.index:
            l.append(int(cnt[c]))
        else:
            l.append(int(0))
    return l,t
from processdata import get_total_times

listt=[]
list2=[]
list3=[]
list4=[]
list5=[]

for day in range(6):
    for i in range(get_total_times(day)):
        l,t=get_station_distribution(day,i)
        listt.append(t)
        list2.append({"value":l[0],"percent":l[0]/394})
        # n=l[1]+l[2]+l[3]+0.01
        list3.append({"value":l[1],"percent":l[1]/394})
        list4.append({"value":l[2],"percent":l[2]/394})
        list5.append({"value":l[3],"percent":l[3]/394})


from pyecharts import options as opts
from pyecharts.charts import Bar,Tab
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

# 绘制车站拥挤度随时间变化
c1 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(listt)
    .add_yaxis("green", list2, stack="stack1", category_gap="0%")
    .add_yaxis("yellow", list3, stack="stack1", category_gap="0%")
    .add_yaxis("orange", list4, stack="stack1", category_gap="0%")
    .add_yaxis("red", list5, stack="stack1", category_gap="00%")
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
        title_opts=opts.TitleOpts(title="station")
    )
    #.render("stack_bar_percent.html")
)

# 绘制站间拥挤度随时间变化

listt=[]
list2=[]
list3=[]
list4=[]
for day in range(6):
    for i in range(get_total_times(day)):
        l,t=get_segment_distribution(day,i)
        listt.append(t)
        list2.append({"value":l[0],"percent":l[0]/922})
        # n=l[1]+l[2]+l[3]+0.01
        list3.append({"value":l[1],"percent":l[1]/922})
        list4.append({"value":l[2],"percent":l[2]/922})


c2 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(listt)
    .add_yaxis("green", list2, stack="stack1", category_gap="0%")
    .add_yaxis("yellow", list3, stack="stack1", category_gap="0%")
    .add_yaxis("red", list4, stack="stack1", category_gap="0%")
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
        title_opts=opts.TitleOpts(title="segment")
    )
    #.render("stack_bar_percent.html")
)
ta=Tab()
ta.add(c1,'station_distribution-time')
ta.add(c2,'segmnet_distribution-time')
ta.render("./charts/stack_bar_percent.html")
