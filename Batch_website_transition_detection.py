#!/usr/bin/env python
#coding:utf-8
#make by xkkhh

import socket
import requests

def urlstatucheck():
   for oneurl in urllist.readlines():
       #example url:http://blog.xkkhh.cn
       
       url=str(oneurl.strip())[7:]
       try:
           ip =socket.gethostbyname(url)
           webstatus = requests.get(url=oneurl.strip(), timeout=10).status_code
           iplist.writelines(oneurl.strip() + " " + str(ip) + " " + str(webstatus) + "\n")
       except:
           print "this url is can not connect"

try:
    urllist=open("C:/Users/Mr.xkkhh/Desktop/url.txt","r")
    iplist=open("C:/Users/Mr.xkkhh/Desktop/urlstatuscheck.txt","w")
    urlstatucheck()
    urllist.close()
    iplist.close()
except:
    print "Error"