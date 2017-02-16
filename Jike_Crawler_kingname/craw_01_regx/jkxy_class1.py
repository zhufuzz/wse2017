# -*- coding: UTF-8 -*-
import sys
import re
print(re.match('www', 'www.runoob.com'))  # 在起始位置匹配
print(re.match('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.match('www', 'www.runoob.com').group())  # 在起始位置匹配
print(re.match('www', 'www.runoob.com').group(0))  # 在起始位置匹配


print(re.match('com', 'www.runoob.com'))         # 不在起始位置匹配



print "#####################################"
line = "Cats are smarter than dogs"

matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)

if matchObj:
   print "matchObj.group() : ", matchObj.group()
   print "matchObj.group(0) : ", matchObj.group(0)
   print "matchObj.group(1) : ", matchObj.group(1)
   print "matchObj.group(2) : ", matchObj.group(2)
else:
   print "No match!!"

print "========================================="

line = "Cats are smarter than dogs";

matchObj = re.match( r'dogs', line, re.M|re.I)
if matchObj:
   print "match --> matchObj.group() : ", matchObj.group()
   print "match --> matchObj.group(0) : ", matchObj.group(0)
   print "match --> matchObj.group(1) : ", matchObj.group(1)
else:
   print "No match!!"

print "-----------------------------------------"

matchObj = re.search( r'dogs', line, re.M|re.I)
if matchObj:
   print "search --> matchObj.group() : ", matchObj.group()
   print "match --> matchObj.group(0) : ", matchObj.group(0)
else:
   print "No match!!"
   
print "-----------------replace replace-----------------"
phone = "2004-959-559 # 这是一个国外电话号码"

# 删除字符串中的 Python注释
num = re.sub(r'#.*$', "", phone)
print "电话号码是: ", num

# 删除非数字(-)的字符串
num = re.sub(r'\D', "", phone)
print "电话号码是 : ", num



