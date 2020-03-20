#!/usr/bin/env python
#coding:utf-8
#make by xkkhh

import requests
import multiprocessing
import re
from sys import argv
import random

user_agent =["Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
"User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"]


def checkStatus(url):
    headers = {"User-Agent": random.choice(user_agent)}
    if 'https' in url:
        res = requests.get(url, headers=headers)
    elif 'http' in url:
        res = requests.get(url, headers=headers)
    else:
        res = requests.get('http://' + url, headers=headers)
    return res

def processCheckStatus(url):
    web = checkStatus(url)
    web.encoding = 'utf-8'
    try:
        print url + ' ' + re.findall('<title>.*</title>', web.text)[0][7:-8] + ' ' + str(web.status_code)
    except:
        pass


if __name__ == "__main__":
    if len(argv) == 1:
        print argv[0] + ' -h for help'
    elif len(argv) >= 2 and argv[1] == '-h':
        print '1.' + argv[0] + ' url \n2.' + argv[0] + ' -r domain.txt processNumber'
    elif len(argv) == 2 and argv[1] != '-h':
        web = checkStatus(argv[1])
        web.encoding = 'utf-8'
        print argv[1] + ' ' + re.findall('<title>.*</title>', web.text)[0][7:-8] + ' ' + str(web.status_code)
    elif len(argv) == 4:
        urls = []
        for lines in open(argv[2]).readlines():
            lines = lines.strip()
            urls.append(lines)
        pool = multiprocessing.Pool(processes=int(argv[3]))
        pool.map(processCheckStatus, urls)
        pool.close()
        pool.join()
    else:
        print 'error'