#encoding=utf-8

class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
    @classmethod
    def get_no_of_instance(cls_obj):
        return cls_obj.no_inst
	
ik1 = Kls()
ik2 = Kls()

print ik1.get_no_of_instance()
print Kls.get_no_of_instance()

'''在Python2.2以后可以使用@classmethod装饰器来创建类方法.
	这样的好处是: 不管这个方式是从实例调用还是从类调用，它都用第一个参数把类传递过来.

'''