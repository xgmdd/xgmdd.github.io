# -*- coding: utf-8 -*-
"""
@author: Issac
"""
import json
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os

def save_page(number:int,day:int):
    
    """进行第day天的第number次爬取，保存页面到本地./output/pages"""

    options = Options()
    # 消除SSL、listening等警告提示输出
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches',['enable-autonation'])
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    options.add_argument("--headless")  # 不打开浏览器界面，以节省时间
    browser = webdriver.Chrome(options=options)

    browser.get('http://map.bjsubway.com')
    browser.maximize_window()
    # 删除这次登录时，浏览器自动储存到本地的cookie
    browser.delete_all_cookies()

    # 读取之前已经储存到本地的cookie
    cookies_filename = './data/cookies_subw.json'
    cookies_file = open(cookies_filename, 'r', encoding='utf-8')
    cookies_list = json.loads(cookies_file.read())
    # print(cookies_list)

    for cookie in cookies_list:  # 把cookie添加到本次连接
        browser.add_cookie({
            'domain': '.map.bjsubway.com',  
            'name': cookie['name'],
            'value': cookie['value'],
            'path': '/',
            'expires': None
        })

    # 再次访问网站，由于cookie的作用，从而实现直接访问
    browser.get("https://map.bjsubway.com")
    time.sleep(2)
    # 点击按钮切换到拥挤度视图
    real_on = browser.find_element(By.ID,"realOff")
    real_on.click()
    time.sleep(1)
    # 按序存储页面
    name='./output/pages/day{}/page_{}.html'.format(day,number)
    t=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    # 打开文件写入页面
    f=open(name,'wb')
    f.write(browser.page_source.encode('utf-8','ignore'))
    f.close()
    # 打开文件写入爬取时间与页面序号的关系
    bo=os.path.exists('./output/tables/number_time/day{}.csv'.format(day))
    f=open('./output/tables/number_time/day{}.csv'.format(day),'a',encoding='utf-8')
    if not bo:
        f.write("num,time\n")
    f.write(str(number) + ',' + t + '\n' )
    f.close()
    # 关闭浏览器
    browser.close()