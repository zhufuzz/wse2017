# -*- coding:utf-8 -*-   x
#while
#while语句使用结构
'''
while 条件为真：
    循环执行“该部分语句
    执行该部分语句
    执行该部分语句”
else：
    如果条件为假，执行该部分语句

#else部分可以省略
'''



#两个简单的while语句实例

#第一个是最简单没有else部分的
'''
a=True
while a:
    print "ABC"
'''

#第二个是有else部分的

b=False
while b:
    print "ABC"
else:
    print "DEF"






    
#我们再来看一下比较复杂一点的有嵌套的while语句
a=1
while a<10:
    if a<=5:
        print a
    else:
        print "hello"
    a=a+1
else:
    print "test"






    

