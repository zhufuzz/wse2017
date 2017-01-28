# -*- coding:utf-8 -*-   x
#特殊方法
#__init__，之前说过，在对象执行时调用
#__del__，之前说过，在对象恰被删除前调用

#__len__，在对对象使用len()函数时调用
'''
class a:
    def x(self):
        pass
    def __len__(self):
        print "我是__len__方法，我出现是因为他们对对象用了len()函数"
'''

#__str__，在对对象使用print语句或str（）时被调用

class a:
    def __str__(self):
        print "我是__str__，我出现代表他们对对象使用了print语句或str()函数"
    def x(self):
        a=8
        b=9
        c=str(a)
        print c

