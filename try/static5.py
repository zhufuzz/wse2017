#encoding=utf-8

'''经常有一些跟类有关系的功能但在运行时又不需要实例和类参
与的情况下需要用到静态方法.
比如更改环境变量或者修改其他类的属性等能用到静态方法.
这种情况可以直接用函数解决, 但这样同样会扩散类内部的代码，
造成维护困难.'''

IND = 'ON'
def checkind():
    return (IND == 'ON')

class Kls(object):
    def __init__(self,data):
        self.data = data
    def do_reset(self):
        if checkind():
            print('Reset done for:', self.data)
    def set_db(self):
        if checkind():
            self.db = 'new db connection'
            print('DB connection made for:',self.data)
		
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()
