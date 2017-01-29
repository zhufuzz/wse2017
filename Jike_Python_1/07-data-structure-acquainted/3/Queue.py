# -*- coding:utf-8 -*-   x
#队列的实现
class Queue():

    def __init__(qu,size):
        qu.queue=[];
        qu.size=size;
        qu.head=-1;
        qu.tail=-1;

    def Empty(qu):
        if qu.head==qu.tail:
            return True
        else:
            return False

    def Full(qu):
        if qu.tail-qu.head+1==qu.size:
            return True
        else:
            return False

    def enQueue(qu,content):
        if qu.Full():
            print "Queue is Full!"
        else:
            qu.queue.append(content)
            qu.tail=qu.tail+1

    def outQueue(qu):
        if qu.Empty():
            print "Queue is Empty!"
        else:
            #result = qu.queue.remove(qu.queue, qu.tail)
            qu.head=qu.head+1

            #return result


q = Queue(6)
print q.Empty()
q.enQueue("1")
print q.Empty()
q.enQueue("2")
q.enQueue("3")
print q.outQueue()
