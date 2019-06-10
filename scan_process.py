from utils import *

def span_text(driver,span_writer):
    spans = driver.find_elements_by_css_selector('[class ="WB_text_opt"]')
    span_urls = []

    req = requests.Session()
    span_driver = webdriver.Chrome('chromedriver')
    login(span_driver,req)

    for span in spans:
        try:
            print("find span")
            span_urls.append(span.get_attribute("href"))
        except Exception as e:
            pass

    print("span urls",span_urls)

    for url in span_urls:
        span_writer.writerow(scan_span(url,span_driver))
    span_driver.quit()
    return

def scan_span(url,span_driver):
    span_driver.get(url)

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
        time = span_driver.find_element_by_xpath(
            '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[4]/div[2]/a').get_attribute(
            "title")
        # time = time_fix(raw_time)
    except:
        try:
            time = span_driver.find_element_by_xpath(
                '//*[@id="Pl_Official_WeiboDetail__73"]/div/div/div/div[1]/div[3]/div[2]/a').get_attribute(
                "title")
            # time = time_fix(raw_time)
        except:
            time = "time error"

    return [user_id, content, share, comment, like, time, pic]