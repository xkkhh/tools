#!/usr/bin/env python
#coding:utf-8
#make_by_xkkhh
#2017年12月16日16:52:10

import sys
import requests
import re

def seartxt():
    '''
    搜索小说
    爬行笔趣阁的小说,没过多的测试。没问题别找我,有问题更别找我!
    '''

    xsm = raw_input("搜索你要下载的小说名:")
    r = requests.get('http://zhannei.baidu.com/cse/search?s=17194782488582577862&entry=1&q='+xsm)    #获取搜索小说名
    r.encoding = "utf-8"
    xsm = re.findall('<a cpos="title" href="(.*) class="result-game-item-title-link" target="_blank">', r.text) #匹配链接

    n = 0
    url = []

    for x in xsm:
        x1 = x[0:39]     #小说链接
        x2 = x[48:-1]    #小说名字
        print str(n)+ '.' + x2
        n += 1
        url.append(x1)

    userurl = url[input("输入序号下载:")]
    downloadtxt(userurl)

def downloadtxt(weburl):
    '''
    下载小说
    爬行笔趣阁的小说,没过多的测试。没问题别找我,有问题更别找我!
    '''
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
            print e.message                                                  #异常处理
            continue

        txtzhang = (txtchapter[0])[(len(txtname))+1:]                       #章节
        txtstr = re.findall(r'&nbsp;&nbsp;&nbsp;&nbsp;(.+)</div>', r1.text) #章节内容

        f1 = open('./' + txtname + '.txt', "a+")                #检查是否写入过该章节
        quchong = f1.read()
        f1.close()

        if (quchong.find(txtzhang) >= 0):
            print "找到重复章节%s跳过.." %txtchapter[0]
        elif (quchong.find(txtzhang) == -1):
            for z in txtstr:
                print "正在写入%s的%s" % (txtname,txtzhang)
                z = z.replace("<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;","\n") #获取内容
                f2 = open('./'+ txtname + '.txt', "a+") #写入文件,追加模式.
                f2.write(txtzhang + "\n" + z + "\n")
                f2.close()
        else:
            print 'Error!'

    print "写入小说%s完成!" % txtname

if __name__ == "__main__":
    seartxt()
