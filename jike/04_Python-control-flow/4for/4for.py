# -*- coding:utf-8 -*-   x
#for语句
'''
for语句格式：
for i in 集合：
    执行该部分
else：
    执行该部分


'''



#第一个for语句
'''
for i in [1,2,8,9,0]:
    print i
'''





#学会使用range函数，第二个for语句
a=range(1,5)
print a
for i in range(1,3):
    print "hello"



for i in range(1,10,3):
    print  i








#最后看一个带嵌套的for语句

for i in range(1,10):
    if i%2==0:
        print i
        print "偶数"
    else:
        print i
        print "奇数"





