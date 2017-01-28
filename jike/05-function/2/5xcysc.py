# -*- coding:utf-8 -*-   x
#函数形参与实参

#参数的概念

#print len()


'''
a="abcdm"
print len(a)
'''



#什么是形参
'''
def function1(a,b):
    if a>b:
        print a
    else:
        print b
   '''     



#什么是实参
'''
def function1(a,b):
    if a>b:
        print a
    else:
        print b
function1(1,3)
'''


#参数的传递
#第一中，最简单的传递
'''
def function(a,b):
    if a>b:
        print "前面这个数大于后面这个数"
    else:
        print "后面这个数比较大"
function(7,8)
'''

#第二种，赋值传递

def function(a,b=8):
    print a
    print b
function(1)
function(1,2)



#关键参数
def function(a=1,b=6,c=7):
    # type: (object, object, object) -> object
    print a
    print b
    print c
#function(5)
#function(b=7,a=8)
#function(5,c=2,b=3)
function(b=4,c=2,a=1)

'''但是要注意，参数不能冲突'''
#function(b=2,c=3,2)







