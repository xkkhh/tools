#!/usr/bin/env python
#coding:utf-8
#make by xkkhh

import urllib2
import re
import time
import sys
import os


def getDesktopPath():
    '''
    适合没修改桌面路径的windows系统
    '''

    return os.path.join(os.path.expanduser("~"), 'Desktop')

def siteWeb(ip):
    '''
    同ip网站查询:siteweb search
    '''

    headers = {"User-Agent":"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    request = urllib2.Request("https://domainbigdata.com/"+ip, headers=headers)
    response = urllib2.urlopen(request,timeout=20).read()
    websitetxt = re.findall(r'(?<=nofollow" href="/).*(?=">)',response)
    t = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    if websitetxt != "":

        desktop = getDesktopPath()+"\\"
        for txt in range(0,len(websitetxt)):

            f = open(desktop + (t+'_'+ip+'_siteweb.txt'),'a+')
            f.write(websitetxt[txt]+"\n")
            f.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:

        print "Use:" + (os.path.basename(sys.argv[0])) + " 1.1.1.1"
    elif len(sys.argv) == 2:

        siteWeb(sys.argv[1])
    else:

        ip = raw_input("Please input the ip address,such as 1.1.1.1:")
        siteWeb(ip)