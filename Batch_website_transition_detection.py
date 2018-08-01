#!/usr/bin/env python
#coding:utf-8
#make by xkkhh

import socket
import requests

def urlstatucheck():
    for oneurl in urllist.readlines():
		cnc = oneurl.replace("\n", "") + " is like can not connect!"
		if oneurl.startswith("http:"):
			url=str(oneurl.strip())[7:]
			try:
				ip =socket.gethostbyname(url)
				webstatus = requests.get(url=oneurl.strip(), timeout=10).status_code
				iplist.writelines(oneurl.strip() + " " + str(ip) + " " + str(webstatus) + "\n")
			except:
				print cnc
		if oneurl.startswith("https:"):
			url=str(oneurl.strip())[8:]
			try:
				ip =socket.gethostbyname(url)
				webstatus = requests.get(url=oneurl.strip(), timeout=10).status_code
				iplist.writelines(oneurl.strip() + " " + str(ip) + " " + str(webstatus) + "\n")
			except:
				print cnc

try:
    #http://www.baidu.com
    #https://www.baidu.com
    urllist=open("C:/Users/Mr.xkkhh/Desktop/url.txt","r")
    iplist=open("C:/Users/Mr.xkkhh/Desktop/urlstatuscheck.txt","w")
    urlstatucheck()
    urllist.close()
    iplist.close()
except:
    print "Error"
