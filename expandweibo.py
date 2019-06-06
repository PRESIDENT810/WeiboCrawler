from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import time
import requests

def getHtml(url, loadmore=True, waittime=10, total_page=20):
    req = requests.Session()
    driver = webdriver.Chrome('chromedriver')
    login(driver,req)
    driver.get(url)
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
            scan_tweets(driver)
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
    driver.find_element_by_xpath('//*[@id="loginname"]').send_keys('3034252785@qq.com')  # 输入用户名
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('residentevil')  # 输入密码
    driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()  # 点击登陆
    cookies = driver.get_cookies()
    add_cookie(cookies, req)
    time.sleep(5)

def add_cookie(cookies,req):
    for cookie in cookies:
        req.cookies.set(cookie['name'], cookie['value'])

def scan_tweets(driver):
    fhand = open('result.txt', 'a')
    post_num = 1
    contents = driver.find_elements_by_css_selector('[class ="WB_text W_f14"]')
    for content in contents:
        print(post_num,content.text)
        fhand.write(str(post_num)+": "+content.text)
        fhand.write('\n')
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