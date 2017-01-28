# -*- coding:utf-8 -*-   x
#break语句
#break语句用法
'''
break语句是强制停止循环执行的意思，break语句用在循环语句中，出现break的地方将直接停止该循环地执行。

'''

#break语句用在while循环中
'''
a=1
while a:
    print a
    a=a+1
    if a==10:
        break
'''

    

#break语句在for循环中
'''
for i in range(5,9):
    print i
    if i>6:
        break
'''


#break语句在双层循环语句中
'''
a=10
while a<=12:
    a=a+1
    for i in range(1,7):
        print i
        if i==5:
            break

'''
        



a=10
while a<=12:
    a=a+1
    for i in range(1,7):
        print i
        if i==5:
            break
    if a==11:
        break 










