class A(object):
    def foo(self, x):
        print("executing foo(%s,%s)" % (self, x))
        print('self:', self)
    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))
        print('cls:', cls)
    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)
a = A()
print(a.foo)
print(a.class_foo)
print(a.static_foo)

print "#########"*3

a.foo(1)
A.foo(a, 1)
A.class_foo(1)
a.class_foo(1)
A.static_foo(1)
a.static_foo(1)

class B(A):
    pass
b = B()
b.foo(1)
b.class_foo(1)
b.static_foo(1)
# executing foo(<__main__.B object at 0x007027D0>,1)
# self: <__main__.B object at 0x007027D0>
# executing class_foo(<class '__main__.B'>,1)
# cls: <class '__main__.B'>
# executing static_foo(1)