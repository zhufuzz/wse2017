# -*- coding:utf-8 -*-   x
#lambda
#1，格式：lambda 参数：表达式
lambda x:x+3

a=lambda x:x+3
a(1)
print a(1)
#print a(27)

#2
b=lambda x,y,z:x+y
c=lambda x,y,z:x+y-z
#b(1)
print b(1,2,3)
#print c(3,2,4)
#上面b用到了两个参数，c用到了3个参数。在传递值的时候，b可以只给两个参数吗？
#print b(1,2)   #答案是不行的，声明了多少个参数，就得给多少个参数，不管是否用到。


#3
def d(t):
    return lambda y:y+t
d1=d(10)                  #d(t)==lambda y:y+t,      d1==d(10)==lambda y:y+10
print d1(7)
#请问以上的步骤中具体的执行过程？
d1=d(10) #这一步中相当于t==10，d1==lambda y:y+10
#print d1(7) #这一步中相当于y=7，然后输出lambda表达式

#习题
#请分析以下程序的输出结果
def m():
    return lambda s:s*3
k=m()
print k("hello")

#请问这样写对吗?为什么？
#print m("hello")

print m()("hi")
