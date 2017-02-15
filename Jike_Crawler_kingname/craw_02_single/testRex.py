#-*-coding:utf8-*-
import re
import requests

f = open('eachClass','r')
html = f.read()
f.close()

print '爬取标题'
title = re.search('<title>(.*?)</title>',html,re.S)
print title

print '爬取链接'
links = re.findall('href="(.*?)"',html,re.S)
for each in links:
     print each

print '抓取部分文字,先大再小'
text_fied = re.findall('<ul>(.*?)</ul>',html,re.S)[0]
the_text = re.findall('">(.*?)</a>',text_fied,re.S)
print text_fied
print the_text