#! /usr/bin/python

import random
import os
# import cgi, cgitb
#
# cgitb.enable()
# form = cgi.FieldStorage()

f = open('/Users/tzh/PycharmProjects/wse2017/ost4/StationEntrances.csv', 'r')

allLines = f.readlines()
f.close()
length = len(allLines)


# s = set()
# for i in allLines:
#     s.add(i)
Station_Names = {}
Station_Latitudes = {}
Station_Latitudes = {}
rounts = {}

#print file_list

#{"station name":[long,lati,line]}
dic = {}
name_set = set()
route_set = set()

for i in range(1, length):
	list = allLines[i].split(',')
	content = {}
	name = list[1] +','+ list[2]
	#print name
	long = list[3]
	#print long
	#lati = list[4]
	#routes = list[5]
	name_set.add(name)
	
	for i in range(3,16):
		content[i] = list[i]
		
	for i in range(6, 16):
		route_set.add(list[i])
	
	
	
	#dic[name] = content
	
	#print dic
	dic[name] = content
	# if dic.has_key(name):
	# 	continue

	#print dic
	#
	
print route_set
print len(name_set)
print len(dic)
print dic.get('Pelham,Elder Av')
print dic.keys()

