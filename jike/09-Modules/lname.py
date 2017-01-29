# -*- coding:utf-8 -*-   x
#-*- coding:UTF-8 -*-
#分别直接执行这个模块与导入这个模块，看一下结果

print __name__
if __name__=="__main__":
        print "This is main"
else:
	print "This is not main"



#import sys
#print sys.path

#from sys import version
#from sys import *

import os
print os.__file__