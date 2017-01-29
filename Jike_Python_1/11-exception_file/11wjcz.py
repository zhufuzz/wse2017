# -*- coding:utf-8 -*-   x
#Python中文件的操作

#创建文件
fc=open("/Users/tzh/Desktop/a.mp3","w")


#打开文件
fo=file("/Users/tzh/Desktop/a.mp8","w")

#写入和关闭文件---写入文件四步曲：先做好内容，然后建立文件，然后再写入，然后再关闭
content='''我是文件的内容
是文件的
内容呢
待会据说要把我写进去。。
'''
fw=file("/Users/tzh/Desktop/a.txt","w")
fw.write(content)
fw.close()

#然后学习了close是关闭之后，我们把a.mp3给关闭了
fc.close()
fo.close()

#读取文件,关键点：先打开文件，在进入while循环依次读取每行
fr=file("/Users/tzh/Desktop/a.txt")
while True:
    line=fr.readline()
    if len(line)==0:
        break
    print line
    fr.close
