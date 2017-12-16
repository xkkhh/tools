#!/usr/bin/env python
#coding:utf-8
#make by xkkhh
#2017年12月16日21:02:17

import sys
import re
import requests

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

def seartxt(xsm, yema = '0'):
    '''
    搜索小说
    爬行笔趣阁的小说,没过多的测试。没问题别找我,有问题更别找我!
    '''

    r = requests.get('http://zhannei.baidu.com/cse/search?q='+ xsm + '&p='+ yema + '&s=920895234054625192&nsid=', headers)  #获取搜索的小说名
    r.encoding = "utf-8"
    #print r.text
    r1 = re.findall('<a cpos="title" href="(.*)" title="', r.text) #匹配小说链接
    r2 = re.findall('" title="(.*)" class="', r.text)              #匹配小说名字
    r3 = re.findall('<span>\s*(.*)\s*</span>', r.text)             #匹配作者

    url = []
    bookname = []
    author = []
    n, n1, n2, n3 = 0, 0, 0, 0

    for x in r1:
        url.append(x)
        n = n + 1
    for x1 in r2:
        bookname.append(x1)
        n1 = n1 + 1
    for x2 in r3:
        author.append(x2)
        n2 = n2 + 1

    print '第'+yema + '页'
    while n3 < len(r1):
        print str(n3) + u'.书名:' + bookname[n3] + u" 作者:" + author[n3]
        n3 += 1
    print "c:上一页 n:下一页 i:自定义页 数字:下载小说"

    search_ordownload = raw_input(":")
    if search_ordownload == "c":
        seartxt(xsm, str(int(yema) - 1))
    elif search_ordownload == "n":
        seartxt(xsm, str(int(yema) + 1))
    elif search_ordownload == "i":
        search_ordownload = raw_input(":")
        seartxt(xsm, search_ordownload)
    elif int(search_ordownload) >= 0:
        downloadtxt(url[int(search_ordownload)])
    else:
        print 'Error'
        exit()

def downloadtxt(url):
    '''
    下载小说
    爬行笔趣阁的小说,没过多的测试。没问题别找我,有问题更别找我!
    '''
    reload(sys)
    sys.setdefaultencoding("utf-8")



    r4 = requests.get(url, headers)
    dirctory = re.findall('<a style="" href="(.*?)">', r4.text)                         #获取全部章节url
    chapter = re.findall('">(.*?)</a></dd>', r4.text)                                   #获取全部章节
    txtname = re.findall('<meta property="og:title" content="(.*?)"/>', r4.text)[0]     #获取书名
    x = 0

    while x <= len(dirctory):
        r5 = requests.get(r'https://www.qu.la' + dirctory[x], headers)
        booktxt = re.findall(u'&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br/>', r5.text)            #获取当前章节文字
        nowchapter = chapter[x]                                                         #当前章节
        f_check = open('./' + txtname + '.txt', "a+")
        check = f_check.read()
        f_check.close()
        if (check.find(nowchapter) >= 0):
            print "找到重复章节%s跳过.." %nowchapter
        elif (check.find(nowchapter) == -1):
            f1 = open('./' + txtname + '.txt', "a+")
            f1.write(nowchapter + "\n")                                                #写入当前章节
            f1.close()
            print '正在写入%s %s' %(txtname, nowchapter)
            for nowbooktxt in booktxt:                                                 #当前文字
                f2 = open('./' + txtname + '.txt', "a+")
                f2.write(nowbooktxt + "\n")                                            #写入当前文字
                f2.close()
        else:
            print 'Error!'
        x += 1
    print "写入小说%s完成!" % txtname

if __name__ == "__main__":
    searchname = raw_input("搜索你要下载的小说名:")
    seartxt(searchname)
