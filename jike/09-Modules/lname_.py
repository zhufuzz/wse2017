# -*- coding:utf-8 -*-   x
#-*- coding:UTF-8 -*-
#首先我们分别看一下这个模块在不同场景中的__name__的值
#print __name__


#其次我们看一下__name__属性的常用情况

if __name__=="__main__":
    print "It's main"
else:
    print "It's not main"

