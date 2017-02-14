#-*-coding:utf8-*-

#导入re库文件
import re
# from re import findall,search,S

	
	
secret_code = 'hadkfalifexxIxxfasdjifja134xxlovexx23345sdfxxyouxx8dfse'


def test1():
	print ".的使用举例"
	a = 'xy123'
	b = re.findall('x...',a)
	print b



def test2():
	print "*的使用举例"
	a = 'xyxy123'
	b = re.findall('x*',a)
	print b



def test3():
	print "?的使用举例"
	a = 'xy123'
	b = re.findall('x?',a)
	print b


def test4():
	print '上面的内容全部都是只需要了解即可，需要掌握的只有下面这一种组合方式(.*?)'
	
	print '.*的使用举例'
	b = re.findall('xx.*xx',secret_code)
	print b
	

def test5():
	print '.*？的使用举例'
	c = re.findall('xx.*?xx',secret_code)
	print c
#
#
#

def test6():
	print '使用括号与不使用括号的差别'
	d = re.findall('xx(.*?)xx',secret_code)
	print d
	for each in d:
		print each
	
def test7():
	print 'test7'
	s = '''sdfxxhello
	xxfsdfxxworldxxasdf'''
	d = re.findall('xx(.*?)xx',s,re.S)
	print d

def test8():
	print '对比findall与search的区别'
	s2 = 'asdfxxIxx123xxlovexxdfd'
	f = re.search('xx(.*?)xx123xx(.*?)xx',s2).group(2)
	print f
	f2 = re.findall('xx(.*?)xx123xx(.*?)xx',s2)
	print f2[0][1]

def test9():
	print 'sub的使用举例'
	s = '123rrrrr123'
	output = re.sub('123(.*?)123','123%d123'%789,s)
	print output

def test10():
	print '演示不同的导入方法'
	info = re.findall('xx(.*?)xx',secret_code)
	for each in info:
		print each
	
def test11():
	print '不要使用compile'
	pattern = 'xx(.*?)xx'
	new_pattern = re.compile(pattern,re.S)
	output = re.findall(new_pattern,secret_code)
	print output

def test12():
	print '匹配数字'
	a = 'asdfasf1234567fasd555fas'
	b = re.findall('(\d+)',a)
	print b

if __name__ == '__main__':
	test1()
	test2()
	test3()
	test4()
	test5()
	test6()
	test7()
	test8()
	test9()
	test10()
	test11()
	