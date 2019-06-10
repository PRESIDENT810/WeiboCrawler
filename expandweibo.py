from scan_process import *
from utils import *

chrome_options = Options()
chrome_options.add_argument('--headless')

def getHtml(url, loadmore=True, waittime=10, total_page=20):
    req = requests.Session()
    driver = webdriver.Chrome('chromedriver')
    login(driver,req)
    driver.get(url)

    file_name = "result{}.csv".format(datetime.datetime.now())
    file = open(file_name,'w')
    writer = csv.writer(file)

    file_name = "span_result{}.csv".format(datetime.datetime.now())
    file = open(file_name,'w')
    span_writer = csv.writer(file)

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
            scan_tweets(driver,writer)
            span_text(driver,span_writer)
        try:
            next_page = driver.find_element_by_css_selector("[class ='page next S_txt1 S_line1']")
            ActionChains(driver).click(next_page).perform()
            time.sleep(waittime)
        except:
            driver.refresh()

    file.close()
    driver.quit()
    # return html

def scan_tweets(driver,csv_writer):
    fhand = open('result.txt', 'a')
    post_num = 1

    contents = driver.find_elements_by_css_selector('[class ="WB_text W_f14"]')

    for i in range(len(contents)):
        content = contents[i].text
        i += 1

        try:
            pic = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[1]/div[3]/div[6]/div/ul'.format(i))
            if 'jpg' in pic.get_attribute('action-data'):
                pic = True
            else:
                pic = False
        except:
            try:
                pic = driver.find_element_by_xpath(
                    '//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[1]/div[4]/div[6]/div/ul'.format(i))
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
            time = driver.find_element_by_xpath('//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[1]/div[3]/div[2]/a'.format(i)).get_attribute("title")
        except:
            try:
                time = driver.find_element_by_xpath(
                    '//*[@id="Pl_Core_MixedFeed__291"]/div/div[3]/div[{}]/div[1]/div[4]/div[2]/a'.format(
                        i)).get_attribute("title")
            except:
                time = "NA"

        # print('\n',"-------------------------------------------"*2,'\n')
        # print("i",i)
        # print("post number",post_num)
        # print("user id: ",user_id)
        # print("content: ",content)
        # print("share",share)
        # print("comment",comment)
        # print("like",like)
        # print("pic number",pic)

        if "展开全文" not in content:
            csv_writer.writerow([user_id,content,share,comment,like,time,pic])
        post_num += 1