#!/usr/bin/env python
#coding:utf-8
#make_by_xkkhh

import sys
import requests
import re


def biquge(weburl, homedir = "./"):
    '爬行笔趣阁的小说,没过多的测试。没问题别找我,有问题更别找我!'
    reload(sys)
    sys.setdefaultencoding("utf-8")

    r = requests.get(weburl)                 #网站最新章节
    r.encoding = "gbk"

    txtname = re.findall('<meta property="og:title" content="(.*?)"/>',r.text)[0] #获取小说名
    dirctory = re.findall('<li><a href="(.*?)">', r.text)                        #获取链接

    for y in dirctory:
        r1 = requests.get("http://www.bqg5200.com/" +y)
        r1.encoding = 'gbk'

        try:
            txtchapter = re.findall(u"<title>(.*?)_笔趣阁</title>", r1.text) #获取章节
        except IndexError,e:
            print e.message                                                              #异常处理
            continue

        txtzhang = (txtchapter[0])[(len(txtname))+1:]
        txtstr = re.findall(r'&nbsp;&nbsp;&nbsp;&nbsp;(.+)</div>', r1.text)

        for z in txtstr:
            print "正在写入%s的%s" % (txtname,txtzhang)
            z = z.replace("<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;","\n") #获取内容
            f = open(homedir + r'\\'+ txtname + '.txt', "a+") #写入文件,追加模式.
            f.write(txtzhang + "\n" + z + "\n")
            f.close()

    print "写入小说%s完成!" % txtname

if __name__ == "__main__":

    if (len(sys.argv) == 1):
        print(r"Use Example:spiderbook.py http://www.bqg5200.com/xiaoshuo/3/3590/ C:\Users\Your'sname\Desktop #默认本程序目录")
    elif (len(sys.argv) == 2):
        biquge(sys.argv[1])
    elif (len(sys.argv) == 3):
        biquge(sys.argv[1], sys.argv[2])
    else:
        print 'Error!'