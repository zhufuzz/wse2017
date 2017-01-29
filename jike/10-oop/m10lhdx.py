# -*- coding:utf-8 -*-   x
#类和对象的实现
#类的实现，建立一个类的格式是：class 类名
class man:
    pass                         #pass属于空语句，无意义，目的是为了保证程序的完整性，叫做占位语句
print man

#对象的实现，建立了类之后，再建立一个类的对象（也叫类的实例），建立对象的方式可以直接在类后面加小括号即可
class woman:
    pass
w=woman()
print w

#以上我们实现了在一个类下创建了一个对象。这里，很多同学会问，之前我们不是说一个类型里面可以有多个例子吗？这里
#为什么只创建了一个对象？包括很多参考书上在这里没有点破，造成了很多初学者对这个问题的困扰。其实，在一个类下确
#实是可以建立多个实例的，我们且看下面的程序：
wangdama=woman()
lidama=woman()
zhangdama=woman()
print wangdama
print lidama
print zhangdama

print wangdama.__dict__
wangdama.toufa="huangse"
print wangdama.__dict__


print lidama.__dict__

print wangdama.__class__.__dict__
wangdama.__class__.xiezi="heise"
print wangdama.__class__.__dict__

print lidama.__class__.__dict__

#这里，很对人可能又会疑问，我们都是将woman()赋给了前面一个实例，那是不是就是说前面这几个实例是一样的呢？
#不是的，我们虽然都是将woman（）赋给了前一个变量（实例），但是具体意义是不一样的。这句话的意思只是说将
#woman这种类型赋给某个对象，只要对象名不一样，那么每个对象所占的存储内存也是不一样的，也就是说，这几个
#对象间可以互不影响。这一点，我们观察每个实例的内存就可知道。

class god:
    def a(self):
        print "sing a song"

zongguan = god()
zongguan.a()
god().a() #通过实例调用


class school:
    def __jiaoxuefangfa(self): #隐藏方法
        print "sssss"
#school().__jiaoxuefangfa()


class people:
    def hi(sefl):
        print 8899
    def __init__(self):
        print "init method"
    def __del__(self):
        a = "how r you"
        b = "find thank you"
        print a + b

p=people()
p.hi()
