# -*- coding: utf-8 -*-
"""
@author: Issac
"""
from getcookies import get_cookies
from savepage import save_page
from time import sleep
# from solvehtml import solve_html 
# from processdata import unique_station
# 使用的树莓派的miniconda环境有无法解决的问题 无法安装pyquest（lxml）只能执行抓取任务不能同时解析 因此不进行解析
# 可由缓存处理中断时间不长的情况
import os
import datetime
import urllib3.exceptions
import selenium.common.exceptions
import pickle

interval=255 # 抓取暂停间隔
total=int(21.5*12) # 按每5min抓取一次每24h的最多次数
totalday=7 # 总天数
nap=int(3.5*3600+120) # 午夜因地铁不运营暂停抓取2.5h

# 缓存读取量的默认值
d,n,t=(0,0,0)
# 尝试查找缓存文件
try:
    f=open("./save/lasttimeinfo.bin",'ab+')
    (d,n,t)=pickle.load(f)
    # 这一次开始页的编号+1
    n=n+1
    print("recovered from ./save/lasttimeinfo.bin : [day{}][pagenum{}][{}]".format(d,n,t))
    f.close()
    
except EOFError:
    print("no cache will be used")



for j in range(d,totalday):
    
    print("waking up day{}".format(j)) # 第{}天开始

    # 新建这一天的文件夹存储页面 防止下面操作文件时因找不到文件夹报错
    if not os.path.exists("./output/pages/day{}".format(j)):
        os.makedirs("./output/pages/day{}".format(j))
    
    for i in range(n,total):
        
        try:
            print("day{} try getting page{}...".format(str(j),str(i)))
            # 保存页面函数
            save_page(i,j)
            # solve_html(i,j)
            # unique_station(i,j)
            # 我的raspi上暂时无法使用
            # 暂停抓取间隔
            print("get a page and start sleeping {}s".format(interval))
            print("current time is "+datetime.datetime.now().strftime('%H:%M:%S') )
            # 255s后再次抓取
            sleep(interval)
        # Alert Text: 地铁非运营时段，暂不提供拥挤度查询！or 加载XML出错！
        except selenium.common.exceptions.UnexpectedAlertPresentException as e:
            if e.alert_text=="地铁非运营时段，暂不提供拥挤度查询！":
                # 求得当前时间 HHMM eg.1923==19:23转化为整数
                t= int(datetime.datetime.now().strftime('%H%M'))
                # 查看t是否在非运营时段（0:40--5:00）
                if t<500 and t>40:
                    # 是则转到一天结束
                    break
            # 否则再试一次
            save_page(i,j)
            # 暂停抓取间隔
            print("get a page and start sleeping {}s".format(interval))
            print("current time is "+datetime.datetime.now().strftime('%H:%M:%S') )
            # 255s后再次抓取
            sleep(interval)

        # cookies失效 等待人工获得cookies
        except urllib3.exceptions.MaxRetryError:
            print("exception happen need regetting cookies manually")
            f= open("./save/lasttimeinfo.bin",'wb')
            pickle.dump((j,i,datetime.datetime.now().strftime('%Y-%M-%D %H:%M:%S')))
            f.close()
            get_cookies()
        # 其他异常
        except Exception as e:
            f= open("./save/lasttimeinfo.bin",'wb')
            pickle.dump((j,i,datetime.datetime.now().strftime('%Y-%M-%D %H:%M:%S')))
            f.close()
            print("-"*20)
            print(e)
            exit(1)
            
            
            

    # 一天结束休息4.5h到次日5:00后左右  
    print("taking nap for 2.5 hours untill 5:00 about...")
    sleep(nap)

