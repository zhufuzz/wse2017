# -*- coding:utf-8 -*-   x
#继承的实现
#比如，一个父亲有两个儿子，大儿子跟小儿子都遗传了父亲的会书法的本事，我们把这种遗传叫继承，
#然后，父亲一般能吃，大儿子却很能吃，小儿子吃得少，这叫做子类继承以外的发展。问，如何写这个代码？
class fuqin:
    def shufa(self):
        print "我会写字…"
class daerzi(fuqin):
    def eat(self):
        print "我还很能吃"
class xiaoerzi(fuqin, daerzi):
    def noeat(self):
        print "我吃得很少"
daerzi=daerzi()
daerzi.shufa()
daerzi.eat()

print daerzi.__class__.__dict__

xiaoerzi=xiaoerzi()
xiaoerzi.shufa()
xiaoerzi.noeat()
xiaoerzi.eat()
#以上大小儿子只继承了父亲的特点，也就是只有一个父类继承，叫做单继承。
#那么，一个子类可以继承多个父类吗？当然是可以的。

#再比如，一头母牛生了两小牛，一牛跟二牛都遗传了母牛会吃草的本事。其次，两头小牛还有一个牛父亲，牛父还会奔跑。
#然后，大牛遗传了牛父的本事，很会奔跑，而二牛没有遗传到牛父奔跑的本事。此时，对于大牛来说，既继承了牛母，也继承
#了牛父，属于多继承。问，如何写这个代码？
class muniu:
    def chicao(self):
        print "我会吃草"
class gongniu:
    def bengpao(self):
        print "我会奔跑"

        def chicao(self):
            print "会吃草"
class daniu(muniu,gongniu):
    pass
class xiaoniu(muniu):
    pass
daniu=daniu()
#daniu.chicao()
#daniu.bengpao()
xiaoniu=xiaoniu()
xiaoniu.chicao()
#xiaoniu.bengpao()

#多继承冲突解决
#接着小牛的例子。我们知道，牛母会吃草，但是牛父其实也会吃草。这个时候问题就来了，两个小牛到底是继承了牛父吃草的
#本领，还是继承了牛母吃草的本领呢？

#我们在上面的程序中，把牛父吃草的功能加上，然后看一下继承的结果

#最终，我们得出结论，当可以继承的父类中出现同名属性或方法的时候，子类到底选择哪个父类的该方法继承，取决于父类的
#优先级，越在左边的父类，该父类的优先级越高
