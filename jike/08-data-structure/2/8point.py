# -*- coding:utf-8 -*-


class jd():
    def __init__(self,data):
        self.data=data
        self.next=None

    
class Linklist():

    def __init__(self,jd2):
        self.head=jd2
        self.head.next=None
        self.tail=self.head

    def add(self,jd2):
        self.tail.next=jd2
        self.tail=self.tail.next

    def view(self):
        jd2=self.head
        linkstr=""
        while jd2 is not None:
            if jd2.next is not None:
                linkstr=linkstr+str(jd2.data)+"-->"
            else:
                linkstr+=str(jd2.data)
            jd2=jd2.next
        print linkstr

jd1=jd(7)
jd2=jd("Hello")
jd3=jd(8899)
x=Linklist(jd1)
x.add(jd3)
x.add(jd2)
x.view()