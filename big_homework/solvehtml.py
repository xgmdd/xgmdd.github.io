# -*- coding: utf-8 -*-
"""
@author: Issac
"""
import os
from pyquery import PyQuery as pq

def solve_html(i:int,day:int):

    """接受天数和页数，找到相应的html page并进行解析
    每解析一个page得到两个csv
    分别位于./output/tables/station和./output/tables/segment
    为站拥挤度和段拥挤度表格"""

    # 创建文件夹以便保存csv文件
    if not os.path.exists("./output/tables/station/day{}".format(day)):
        os.makedirs("./output/tables/station/day{}".format(day))
    if not os.path.exists("./output/tables/segment/day{}".format(day)):
        os.makedirs("./output/tables/segment/day{}".format(day))
    # 开始解析
    pq_doc = pq(filename='./output/pages/day{}/page_{}.html'.format(day,i),encoding='utf-8')
    # 打开车站拥挤度表格
    node_file = open('./output/tables/station/day{}/page_{}.csv'.format(day,str(i)), 'w', encoding='utf-8')
    # 写入表头
    node_file.write('name' + ',' + 'color' + '\n')
    # 找到代表车站的元素
    pq_items = pq_doc('#SvgjsG1010 circle')
    item_list = pq_items.items()

    # print('-'*10)
    
    # dic = {'#79be85':'green','#ecce39':'yellow','#de7009':'orange','#f20a0a':'red'} # or black（red）
    # 颜色翻译如上
    # 遍历“生成器”中的所有节点元素，获取节点的属性，并写入
    for item in item_list:
        node_file.write(item.attr('sdata') + ',' + item.attr('fill') + '\n')
    node_file.close()

    # print("done station data")
    # print('-'*10)
    # 打开列车运段拥挤度表格 同理
    node_file = open('./output/tables/segment/day{}/page_{}.csv'.format(day,str(i)), 'w', encoding='utf-8')
    # 出发站-停止站-拥挤度
    node_file.write('seg_from' + ',' + 'seg_to' + ',' + 'color' + '\n')
    # line可以表示两站之间的线段
    pq_items = pq_doc('#SvgjsG1010 line')
    item_list = pq_items.items()
    for item in item_list:
        node_file.write(item.attr('sdata') + '\n')
    # 也有的站间用的path
    pq_items = pq_doc('#SvgjsG1010 path')
    item_list = pq_items.items()
    # 写入文件（此时含重）
    for item in item_list:
        node_file.write(item.attr('sdata') + '\n')
    node_file.close()
    # print("done seg data{}".format(i))
    # print('-'*10)


from processdata import get_total_times

for i in range(6):
    for j in range(get_total_times(i)):
        try:
            solve_html(j,i)
        except Exception as e:
            print(e)
    print("done solving day{}".format(i))


