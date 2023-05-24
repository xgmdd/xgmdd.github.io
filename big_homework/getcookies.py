# -*- coding: utf-8 -*-
"""
@author: Issac
"""
'''
由于bjsubway存在反爬selenium，因此配合手工操作登录，获取cookies，保存到本地，以备后续使用
'''
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #用于设置浏览器启动的一些参数
import time
def get_cookies():
    """配合手动输入访问，保证获得有效map.bjsubway.com的cookies
    并保存到'./data/cookies_subw.json'"""
    options = Options()
    browser = webdriver.Chrome(options=options)
    browser.get('http://www.baidu.com')
    browser.maximize_window()

    input("请用手动输入map.bjsubway.com进入页面，然后按回车……")  # 等待用登录, 登录后回车即可

    cookies_dict = browser.get_cookies()
    cookies_json = json.dumps(cookies_dict)
    # print(cookies_json)

    # 登录完成后,将cookies保存到本地文件
    out_filename = './data/cookies_subw.json'
    out_file = open(out_filename, 'w', encoding='utf-8')
    out_file.write(cookies_json)
    out_file.close()
    print('Cookies文件已写入：' + out_filename)

    time.sleep(3)
    browser.close()



