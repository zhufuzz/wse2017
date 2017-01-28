# -*- coding:utf-8 -*-   x
#continue的使用

#continue语句的使用
'''
continue语句是放在循环语句中的，用来结束本次循环的语句。
'''

#continue语句在while循环中
#首先我们得知道循环是分很多次的，而continue语句是终止该次循环，而不是终止该循环。
'''
a=1
while a<7:
    a=a+1
    if a==3:
        continue
    print a
'''



#continue语句在for循环中,并比较以下两个程序a和程序b
#程序a
'''
for i in range(1,7):
    if i==3:
        continue
    print i
'''

#程序b
'''
for i in range(1,7):
    print i
    if i==3:
        continue
 '''

#continue语句在双层循环语句中
'''
a=1
while a<7:
    a=a+1
    if a==4:
        continue 
    for i in range(7,10):
        if i==9:
            continue
        print i
'''




#continue语句与break语句的区别
'''
continue语句指的是结束执行本次循环中剩余的语句，然后继续下一轮的循环。
而break语句指的是直接结束这个循环，包括结束执行该循环地剩余的所有次循环。
'''
#区分程序c和程序d

#程序c
'''
for i in range(10,19):
    if i==15:
        continue
    print i
'''

#程序d

for i in range(10,19):
    if i==15:
        break
    print i





