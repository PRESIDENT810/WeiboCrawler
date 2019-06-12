from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import time
import requests
import csv
import datetime
import re
from selenium.webdriver.chrome.options import Options

def login(driver,req):
    driver.get("http://www.weibo.com/login.php")
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys('username')  # 输入用户名
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('password')  # 输入密码
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()  # 点击登陆
    cookies = driver.get_cookies()
    add_cookie(cookies, req)
    time.sleep(2)

def add_cookie(cookies,req):
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie['value'])

def time_fix(time_string):
    now_time = datetime.datetime.now()
    if '秒前' in time_string:
        minutes = re.search(r'^(\d+)秒', time_string).group(1)
        created_at = now_time - datetime.timedelta(seconds=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '分钟前' in time_string:
        minutes = re.search(r'^(\d+)分钟', time_string).group(1)
        created_at = now_time - datetime.timedelta(minutes=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '小时前' in time_string:
        minutes = re.search(r'^(\d+)小时', time_string).group(1)
        created_at = now_time - datetime.timedelta(hours=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '今天' in time_string:
        return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

    if '月' in time_string:
        time_string = time_string.replace('月', '-').replace('日', '')
        time_string = str(now_time.year) + '-' + time_string
        return time_string

    return time_string