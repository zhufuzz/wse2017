#-*_coding:utf8-*-
import requests
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spider(object):
    def __init__(self):
        print u'�碉拷���ユ�ㄩ���ゆ�烽���ゆ�烽���ゆ�烽����锟界�扮�����ゆ�烽���ゆ�烽���ゆ��'

#getsource��濮�锟斤拷��濮�锟斤拷�����查���ゆ�风�锟介���ャ��锟斤拷���ワ拷��锟介���ゆ��
    def getsource(self,url):
        html = requests.get(url)
        # print html.text
        return html.text

#changepage��濮�锟斤拷��濮�锟窖��烽���ワ拷锟介���ゆ�烽���ャ��锟斤拷���ワ拷锟介���ゆ�烽����锟斤拷���ゆ��
    def changepage(self,url,total_page):
        now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
            page_group.append(link)
        return page_group
	
#geteveryclass��濮�锟斤拷��濮�锟斤拷���ゆ�烽���ゆ�锋慨锝��峰�锟介����锟斤拷锟窖��烽���ゆ�烽���ゆ�峰ǎ锟斤拷锟介���ゆ��
    def geteveryclass(self,source):
        everyclass = re.findall('<li id=".*?" test="0" deg="0" >.*?</li>',source,re.S)
        print everyclass
        return everyclass
	
#getinfo��濮�锟斤拷��濮�锟姐���锋慨锝��峰�锟介����锟斤拷锟窖��烽���ゆ�峰�锟介���ゆ�烽���ゆ�烽���ゆ�凤拷锟介���ゆ�峰ù锟介���ゆ�烽����锟斤拷���ゆ�烽���ワ拷锟斤拷���ゆ��
    def getinfo(self,eachclass):
        info = {}
        info['title'] = re.search('target="_blank">(.*?)</a>',eachclass,re.S).group(1)
        info['content'] = re.search('</h2><p>(.*?)</p>',eachclass,re.S).group(1)
        timeandlevel = re.findall('<em>(.*?)</em>',eachclass,re.S)
        info['classtime'] = timeandlevel[0]
        info['classlevel'] = timeandlevel[1]
        info['learnnum'] = re.search('"learn-number">(.*?)</em>',eachclass,re.S).group(1)
        return info
	
#saveinfo��濮�锟斤拷��濮�锟姐���凤拷锟介����锟介���ゆ�烽���ゆ�烽��锟�info.txt���ゆ�峰ù锟斤拷浣�锟斤拷
    def saveinfo(self,classinfo):
        f = open('info.txt','a')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('content:' + each['content'] + '\n')
            f.writelines('classtime:' + each['classtime'] + '\n')
            f.writelines('classlevel:' + each['classlevel'] + '\n')
            f.writelines('learnnum:' + each['learnnum'] +'\n\n')
        f.close()
		
    def savehtml(self,html):
        f = open('html.html','a')
        f.write(html)
        f.close()


if __name__ == '__main__':

    classinfo = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    jikespider = spider()
    all_links = jikespider.changepage(url,1)
    for link in all_links:
        print u'婵�锟介��锟介��濮�锟姐���烽���ゆ�峰���锟介�╂�烽��浠�锟斤拷��锟�' + link
        html = jikespider.getsource(link)
        jikespider.savehtml(html)
        everyclass = jikespider.geteveryclass(html)
		
        for each in everyclass:
            info = jikespider.getinfo(each)
            # print info
            classinfo.append(info)
    jikespider.saveinfo(classinfo)


