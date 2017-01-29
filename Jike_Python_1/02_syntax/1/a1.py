# coding=GB2312
print("This line will be printed.")


students=["xiaoming", "xiaohua", "xiaoli", "xiaojuan", "xiaoyun"]
print students[3]

print students

students[1] = "bruce"

print students

print "==================set===================="
a=set("abcnmaaaaaggsng")
print  a

b=set("cdfm")
print b
x=a&b
print x
y=a|b
print y
z=a-b
print z
new=set(students)
print new

print "=================dictionary====================="

zidian={'name':'weiwei', 'home':'guilin','like':'music'}

print zidian
print zidian['name']
zidian['hehe'] = 'xixi'
print zidian


zidian2 ={"姓名":"微微","籍贯":"桂林"}
print zidian2

zidian2["爱好"]="音乐"
print zidian2


