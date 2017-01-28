# -*- coding:utf-8 -*-   x
#"+":两个对象相加
#两个数字相加
a=7+8
#$print a

#两个字符串相加
b="GOOD"+" JOB!"
#print b

#"-":取一个数字的相反数或者实现两个数字相减
a=-7
#print a
b=-(-8)
#print b

c=19-1
#print c


#"*":两个数相乘或者字符串重复
a=4*7
#print a

b="hello"*7
#print b


#"/":两个数字相除
a=7/2
#print a

b=7.0/2
c=7/2.0
#print b
#print c


#"**":求幂运算
a=2**3   #相当于2的3次幂，就是2*2*2
#print a



#"<"：小于符号，返回一个bool值
a=3<7
#print a

b=3<3
#print b

#">":大于符号，返回一个bool值
a=3>7
#print a

b=3>1
#print b




#"!=":不等于符号，同样返回一个bool值
a=2!=3
#print a

b=2!=2
#print b



#"//":除法运算，然后返回其商的整数部分，舍掉余数
a=10//3
#print a

#"%":除法运算，然后返回其商的余数部分，舍掉商
a=10%3
#print a

b=10%1  #没有余数的时候返回什么？
#print b


a=10//3  #a为商的整数部分
b=10%3   #b为
c=3*a+b  #c为除数乘以商的整数部分加上余数，应该c的值就是被除数
#print c



#"&":按位与运算，所谓的按位与是指一个数字转化为二进制，然后这些二进制的数按位来进行与运算




a=7&18  #执行一下，为什么7跟18与会得到2呢？？
#print a
'''首先我们打开计算器，然后我们将7转化为二进制，得到7的二进制值是：111，自动补全为8位，即00000111
   然后我们将18转化为二进制，得到18二进制的值是10010，同样补全为8位，即00010010
   再然后，我们将00000111
   ，跟        00010010按位进行与运算，
   得到的结果是：00000010，然后，我们将00000010转化为十进制
   得到数字二，所以7跟18按位与的结果是二进制的10，即为十进制的2

'''




#"|":按位或运算，同样我们要将数字转化为二进制之后按位进行或运算
a=7|18
#print a
'''我们来分析一下，同样我们的7的二进制形式是00000111，18的二进制形式是00010010
   我们将      00000111
   跟         00010010按位进行或运算，
   得到的结果是 00010111，然后，我们将00010111转化为十进制
   得到数字23，所以7跟18按位或的结果是二进制的10111，即为十进制的23


'''



#"^"按位异或
a=7^18
#print a
'''
   首先，异或指的是，不同则为1，相同则为0.
   我们来分析一下，同样我们的7的二进制形式是00000111，18的二进制形式是00010010
   我们将      00000111
   跟         00010010按位进行异或运算，
   得到的结果是 00010101，然后，我们将00010101转化为十进制
   得到数字21，所以7跟18按位异或的结果是二进制的10101，即为十进制的21


'''

#"~":按位翻转~x=-（x+1）
a=~18  #~18=-（18+1）=-19
#print a


#"<<":左移
'''
比如18左移就是将他的二进制形式00100100左移，即移后成为00100100，即成为36，左移一个单位相当于乘2,左移动两个单位
相当于乘4，左移3个单位相当于乘8，左移n个单位相当于乘2的n次幂。
'''
a=18<<1
#print a

b=3<<3
#print b




#"<<"：右移
'''
右移是左移的逆运算，即将对应的二进制数向右移动，右移一个单位相当于除以2,右移动两个单位相当于除以4，右移3个单位相当于
除以8，右移n个单位相当于除以2的n次幂。
'''
a=18>>1
#print a

b=18>>2
#print b


#"<=":小于等于符号，比较运算，小于或等于，返回一个bool值
a=3<=3#print a

b=4<=3
#print b

#">="
a=1>=3
#print a

b=4>=3
#print b

#"==":比较两个对象是否相等
a=12==13
#print a

b="hello"=="hello"
#print b

#not:逻辑非
a=True
b=not a
#print b

c=False
#print not c

#and:逻辑与
'''
True and True等于True
True and False等于False
False and True等于False
'''
#print True and True


#or:逻辑或
'''
True and True等于True
True and False等于True
False and False等于False
'''
print True or False

