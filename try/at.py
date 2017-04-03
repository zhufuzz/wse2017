#encoding=utf-8

def shout(word="yes"):
    return word.capitalize()+"!"

print shout()
# outputs : 'Yes!'

# 作为一个对象，你可以讲函数赋值给另一个对象
scream = shout

# 注意到这里我们并没有使用括号：我们不是调用函数，而是将函数'shout'赋给变量'scream'
# 这意味着，你可以通过'scream'调用'shout'

print scream()
# outputs : 'Yes!'

# 不仅如此，你可以删除老的名称'shout'，但是通过'scream'依旧可以访问原有函数

del shout
try:
    print shout()
except NameError, e:
    print e
    #outputs: "name 'shout' is not defined"

print scream()
# outputs: 'Yes!'