import requests
import expandweibo
import csv
import time
import sys
from datetime import datetime
from threading import Timer

def getTweets():
    pages = int(sys.argv[1])
    login = False
    url = "https://weibo.com/p/100808c26dbde663d888f8d782f12790f8b5fb/super_index"
    response = requests.get(url)
    # time.sleep(3)
    html = response.text
    html = expandweibo.getHtml(url,total_page=pages)

def main():
    inc = 60*int(sys.argv[2])
    circulation(inc)

def circulation(inc):
    getTweets()
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    t = Timer(inc, circulation, (inc,))
    t.start()

main()