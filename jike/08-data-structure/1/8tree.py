# -*- coding:utf-8 -*-   x
#树

#树的基本构造
Tree=[2,3,[58,6,[5]]]
print Tree[0]
#print Tree[1]
print Tree[2]
Tree2=Tree[2]
print Tree2[0]

#二叉树的构造
'''
比如要构造一个二叉树：
      7
 8        9
   23    36
57 58
可以这样分析：
base=(-->8也就是jd2,-->9也就是jd3,base)
jd2=(no,-->23也就是jd4,8)
jd3=(no,-->36也就是jd5,9)
jd4=(-->57也就是jd6,-->58也就是jd7,23)
jd5=(no,no,36)
jd6=(no,no,57)
jd7=(no,no,58)
但是要注意，写的时候倒过来写。
'''


class TRee():

    def __init__(self,leftjd=0,rightjd=0,data=0):
        self.leftjd=leftjd;
        self.rightjd=rightjd;
        self.data=data;


class Btree():

    def __init__(self,base=0):
        self.base=base

    def empty(self):
        if self.base is 0:
            return True
        else:
            return False

    def qout(self,jd):
        """前序遍历，NLR，根左右"""
        if jd==0:
            return
        print jd.data
        self.qout(jd.leftjd)
        self.qout(jd.rightjd)

    def mout(self,jd):
        """中序遍历，LNR，左根右"""
        if jd==0:
            return
        self.mout(jd.leftjd)
        print jd.data
        self.mout(jd.rightjd)

    def hout(self,jd):
        """后序遍历，LRN，左右根"""
        if jd==0:
            return
        self.hout(jd.leftjd)
        self.hout(jd.rightjd)
        print jd.data

jd1=TRee(data=8)
jd2=TRee(data=9)
base=TRee(jd1,jd2,7)
x=Btree(base)
x.qout(x.base)
