#! /usr/bin/python

import random
import os
import cgi, cgitb
cgitb.enable()
form = cgi.FieldStorage()
f = open('/web/tz406/cgi-bin/StationEntrances.csv', 'r')
#f = open('/Users/tzh/Downloads/StationEntrances.csv', 'r')

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
routes = []
for i in range(1, length):
	list = allLines[i].split(',')
	content = []
	name = list[1] +','+ list[2]
	name_set.add(name)
	content.append(list[3])
	content.append(list[4])
	for i in range(5,16):
		if list[i] !=  '':
			content.append(list[i])
	for i in range(6, 16):
		route_set.add(list[i])
	dic[name] = content

#print dic
#exit(0)

name_list = []
for i in name_set:
	if i != '':
		name_list.append(i)
#random.shuffle(name_list)


route_list = []
for i in route_set:
	if i != '':
		route_list.append(i)

QandA  = {}
correct_names = []
correct_route_lists = []
wrong_route_lists = []
coordinates = []

numQuestions = 2

for i in range(0,numQuestions):
	name = name_list[i]
	#print name
	correct_names.append(name)
	
	coordinate = []
	coordinate.append(dic[name][0])
	coordinate.append(dic[name][1])
	coordinates.append(coordinate)
	#print coordinate

	correct_route_list = []
	for i in range(2, len(dic[name])):
		correct_route_list.append(dic[name][i])
		
	wrong_route_set = route_set - set(correct_route_list)
	wrong_route_list = []
	for i in wrong_route_set:
		if i != '':
			wrong_route_list.append(i)
	wrong_route_lists.append(wrong_route_list)
	correct_route_lists.append(correct_route_list)
	
	#print correct_route_list
	#print wrong_route_list
	
#print name_list[i]
#print answers
#print coordinates
#print otherChoices

#exit(0)
answers = []

# print "Content-type:text/html\n\n"
# print "<h1> MTA Subway Quiz</h1>"
print "Content-type:text/html\n\n"

if os.environ['REQUEST_METHOD'] == 'GET':
	print "<html>"
	print "<body>"
	print "<h2>MTA Quiz</h2><FORM ACTION=hw4.cgi METHOD=POST><OL>"
	c = 0.0011
	
	for i in range(0,numQuestions):
		print 'Question '+str(i+1)
		station_name = correct_names[i].split(',')[0]
		#print 'Which line stops at '+station_name+'?'
		
		print "<p><li><b>" + 'Which line stops at '+station_name+'?'
		#station_name = correct_names.split(',')[0]
		longitude =  coordinates[i][0]
		latitude =   coordinates[i][1]
		long_minus_c =  float(longitude) - c
		lati_minus_c =  float(latitude) - c
		long_plus_c  = float(longitude) + c
		lati_plus_c =  float(latitude) + c
		
		choices = []
		random.shuffle(correct_route_lists[i])
		answer = correct_route_lists[i][0]
		choices.append(answer)
		random.shuffle(wrong_route_lists[i])
		for j in range(0,3):
			choices.append(wrong_route_lists[i][j])
		random.shuffle(choices)
		#print choices
		
		print "<p>"
		print '<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"'+'src="http://www.openstreetmap.org/export/embed.html?bbox='+str(lati_minus_c)+','+str(long_minus_c)+','+str(lati_plus_c)+','+str(long_plus_c)+'&layer=hot&marker='+str(longitude)+','+str(latitude)+'"'+'style="border: 1px solid black"></iframe>'
		print "<p>"
		
		
		print "<input type=hidden name=s"+str(i)+"value="+station_name+">"
		#print '< input type = "hidden" name =a' + str(i) + ' value = '+station_name+'>'
		#print '< input type = "hidden" name =s' + str(i) + ' value = "34th St" >'
		print "<input type=hidden name=a"+str(i)+"value ="+answer+">"
		#print '< input type = "hidden" name =s' + str(i) + ' value = '+station_name+'>'
		
		for j in range(0, 4):
			print "<input type=radio name=q"+str(i)+" value="+choices[j]+">"+choices[j]+"<br>"
		

		
		
		print "</li>"
		
print "</OL><INPUT TYPE=SUBMIT VALUE=Grade></FORM>"
print "</body>"
print "</html>"

if os.environ['REQUEST_METHOD'] == 'POST':
	numCorrect = 0
	numWrong = 0
	correctAnswers = []
	wrongAnswers = []
	for i in range(0, numQuestions):
		#print form["q"+str(i)].value
		#print form["q"+str(i)]
		if form["q"+str(i)].value in correct_route_lists[i]:
			numCorrect += 1
			correctAnswers.append(name_list[i])
		else:
			numWrong += 1
			wrongAnswers.append(form["q"+str(i)].value)

	# layout
	print "<html>"
	print "<body>"
	print "submit"
	print "You got <b>" + str(numCorrect) + " of " + str(numCorrect+numWrong) + "</b> answers correct."
	print "<p><table border=1>"
	print "<tr>"
	print "<th>Correct</th>"
	print "<th>Incorrect</th>"
	print "</tr>"
	print "<tr>"
	print "<td valign=top><font color=green>"
	for i in range(0, len(correctAnswers)):
		print correctAnswers[i] + " <br>"
	print "</font></td>"
	print "<td valign=top><font color=red>"
	for j in range(0, len(wrongAnswers)):
		print wrongAnswers[j] + " <br>"
	print "</font></td></tr></table>"
	print "</body>"
	print "</html>"
	