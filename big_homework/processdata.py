# -*- coding: utf-8 -*-
"""
@author: Issac
"""


def get_total_times(day:int):
    """返回day天的爬取次数"""
    return len(open('./output/tables/number_time/day{}.csv'.format(day),'r',encoding='utf-8').readlines())-1
