from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import time
import requests
import csv
import datetime
import re

def getHtml(url, loadmore=True, waittime=10, total_page=20):
    req = requests.Session()
    driver = webdriver.Chrome('chromedriver')
    login(driver,req)
    driver.get(url)
    file_name = "result{}.csv".format(datetime.datetime.now())
    file = open(file_name,'w')
    writer = csv.writer(file)
    for page_cnt in range(total_page):
        cnt = 0
        if loadmore:
            while True:
                try:
                    js = "document.documentElement.scrollTop=250000"
                    driver.execute_script(js)
                    time.sleep(waittime)
                    cnt += 1
                    print("page {}, span part {}".format(page_cnt,cnt))
                    if cnt == 5:
                        break
                except:
                    break
            span_text(driver)
            scan_tweets(driver,writer)
        try:
            next_page = driver.find_element_by_css_selector("[class ='page next S_txt1 S_line1']")
            ActionChains(driver).click(next_page).perform()
            time.sleep(waittime)
        except selenium.common.exceptions.NoSuchElementException:
            driver.refresh()
            # for i in range(10):
            #     js = "document.documentElement.scrollTop=250000"
            #     driver.execute_script(js)
            #     time.sleep(15)
            # next_page = driver.find_element_by_css_selector("[class ='page next S_txt1 S_line1']")
            # ActionChains(driver).click(next_page).perform()
            # time.sleep(waittime)

    driver.quit()
    # return html

def login(driver,req):
    driver.get("http://www.weibo.com/login.php")
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys('user-id')  # 输入用户名
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('password')  # 输入密码
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()  # 点击登陆
    cookies = driver.get_cookies()
    add_cookie(cookies, req)
    time.sleep(5)

def add_cookie(cookies,req):
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie['value'])

def scan_tweets(driver,csv_writer):
    fhand = open('result.txt', 'a')
    post_num = 1

    contents = driver.find_elements_by_css_selector('[class ="WB_text W_f14"]')
    # shares = driver.find_elements_by_css_selector('[class="W_ficon ficon_forward S_ficon"]')
    # comments = driver.find_elements_by_css_selector('[class="W_ficon ficon_repeat S_ficon"]')
    # likes = driver.find_elements_by_css_selector('[class="W_ficon ficon_praised S_txt2"]')

    for i in range(len(contents)):
        content = contents[i].text
        # path = contents[i].location

        try:
            pic = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[1]/div[3]/div[6]/div/ul'.format(i))
            if 'jpg' in pic.get_attribute('action-data'):
                pic = True
            else:
                pic = False
        except:
            pic = False
        try:
            user_id = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]'.format(i)).get_attribute("tbinfo")[5:]
        except:
            user_id = "NA"
        try:
            share = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[2]/div/ul/li[2]/a/span/span/span/em[2]'.format(i)).text
        except:
            share = 0
        try:
            comment = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[2]/div/ul/li[3]/a/span/span/span/em[2]'.format(i)).text
        except:
            comment = 0
        try:
            like = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[2]/div/ul/li[4]/a/span/span/span/em[2]'.format(i)).text
        except:
            like = 0
        try:
            raw_time = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[1]/div[3]/div[2]/a'.format(i)).text
            time = time_fix(raw_time)
        except:
            time = "NA"

        # share = shares[i].text
        # comment = comments[i].text
        # like = likes[i].text
        print(user_id)
        print(post_num,content)
        print(share)
        print(comment)
        print(like)
        # fhand.write(str(post_num)+": "+content)
        # fhand.write('\n')
        csv_writer.writerow([user_id,content,share,comment,like,time,pic])
        post_num += 1

    # fhand = open('result.txt', 'a')
    # post_num = 1
    # while post_num!=50:
    #     try:
    #         content = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[1]/div[3]/div[4]'.format(post_num))
    #         print("content",post_num,content.text)
    #         fhand.write(str(post_num)+": "+content.text+'\n')
    #         post_num+=1
    #     except:
    #         post_num+=1
    #         continue

def span_text(driver):
    spans = driver.find_elements_by_css_selector('[class ="WB_text_opt"]')
    for span in spans:
        try:
            print("find span")
            ActionChains(driver).click(span).perform()
            time.sleep(5)
        except Exception as e:
            pass

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
