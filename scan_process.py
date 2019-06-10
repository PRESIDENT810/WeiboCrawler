from utils import *
import time

def handle_span(url_list,writer):
    # fhand = open(name,'r')
    # url_list = fhand.read().split('\n')[:-1]

    print("handle span",url_list)
    req = requests.Session()
    span_driver = webdriver.Chrome('chromedriver')
    login(span_driver,req)
    time.sleep(6)

    # file_name = "span_result{}.csv".format(datetime.datetime.now())
    # file = open(file_name,'w')
    # writer = csv.writer(file)

    for url in url_list:
        time.sleep(3)
        scan_span(url,writer,span_driver)

def scan_span(url,span_writer,span_driver):
    print(url)

    span_driver.get(url)
    # time.sleep(6)
    time.sleep(3)

    try:
        content = span_driver.find_element_by_xpath('//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[4]/div[4]').text
    except:
        try:
            content = span_driver.find_element_by_xpath(
                '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[3]/div[4]').text
        except:
            content = "content error"

    try:
        pic = span_driver.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[4]/div[5]/div/div[2]/div[1]/ul/li/div/div[1]')
        print(pic.get_attribute('src'))
        if 'jpg' in pic.get_attribute('src-data'):
            pic = True
        else:
            pic = False
    except:
        try:
            pic = span_driver.find_element_by_xpath(
                '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[3]/div[5]/div/div[2]/div[1]/ul/li/div/div[1]')
            print(pic.get_attribute('src'))
            if 'jpg' in pic.get_attribute('src-data'):
                pic = True
            else:
                pic = False
        except:
            pic = False

    try:
        user_id = span_driver.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div').get_attribute("tbinfo")[5:]
    except:
        user_id = "NA"
    try:
        share = span_driver.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[2]/div/ul/li[2]/a/span/span/span/em[2]').text
    except:
        share = 0
    try:
        comment = span_driver.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[2]/div/ul/li[3]/a/span/span/span/em[2]').text
    except:
        comment = 0
    try:
        like = span_driver.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[2]/div/ul/li[4]/a/span/span/span/em[2]').text
    except:
        like = 0

    try:
        tweet_time = span_driver.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[4]/div[2]/a').get_attribute(
            "title")
        # time = time_fix(raw_time)
    except:
        try:
            tweet_time = span_driver.find_element_by_xpath(
                '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[3]/div[2]/a').get_attribute(
                "title")
            # time = time_fix(raw_time)
        except:
            tweet_time = "time error"

    result = [user_id, content, share, comment, like, tweet_time, pic]
    print(result)
    span_writer.writerow([user_id, content, share, comment, like, tweet_time, pic])
    span_driver.quit()
    return

if __name__ == "__main__":
    fhand = open("test.txt",'r')
    url_list = fhand.read().split('\n')[:-1]
    print(url_list)

    # req = requests.Session()
    # driver = webdriver.Chrome('chromedriver')
    # login(driver,req)

    file_name = "span_result{}.csv".format(datetime.datetime.now())
    file = open(file_name,'w')
    writer = csv.writer(file)

    for url in url_list:
        scan_span(url,writer)