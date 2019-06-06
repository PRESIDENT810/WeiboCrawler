import requests
import expandweibo
import csv
import time
import sys

def getTweets():
    pages = int(sys.argv[1])
    login = False
    url = "https://weibo.com/p/1008082a98366b6a3546bd16e9da0571e34b84/super_index"
    response = requests.get(url)
    # time.sleep(3)
    html = response.text
    html = expandweibo.getHtml(url,total_page=pages)

getTweets()