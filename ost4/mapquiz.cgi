#! /usr/bin/python

import random
import os
import cgi, cgitb
cgitb.enable()
form = cgi.FieldStorage()
f = open('/web/tz406/cgi-bin/StationEntrances.csv', 'r')

#read all lines from file, since file is small
allLines = f.readlines()
f.close()
length = len(allLines)

dic = {}
name_set = set()
route_set = set()
routes = []

#create dictionary from all lines
#use station name as key
#longitude, latitude, routes as value
#also create name_set which has unique station names
#create route_set which has unique route names
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

#get name_list from name_set
name_list = []
for i in name_set:
	if i != '':
		name_list.append(i)
random.shuffle(name_list)

#get route_list from route_set
route_list = []
for i in route_set:
	if i != '':
		route_list.append(i)

correct_names = []
correct_route_lists = []
wrong_route_lists = []
coordinates = []

numQuestions = 5
numChoices = 4
for i in range(0,numQuestions):
	#choose one name in the name_list as correct answer
	name = name_list[i]
	correct_names.append(name)
	#get the coordinates of this station
	coordinate = []
	coordinate.append(dic[name][0])
	coordinate.append(dic[name][1])
	coordinates.append(coordinate)
	#get all the possible correct routes at this station
	correct_route_list = []
	for i in range(2, len(dic[name])):
		correct_route_list.append(dic[name][i])
	#get all the possible wrong routes at this station
	wrong_route_set = route_set - set(correct_route_list)
	wrong_route_list = []
	for i in wrong_route_set:
		if i != '':
			wrong_route_list.append(i)
	wrong_route_lists.append(wrong_route_list)
	correct_route_lists.append(correct_route_list)

answers = []

print "Content-type:text/html\n\n"

#default web page
if os.environ['REQUEST_METHOD'] == 'GET':
	print "<html>"
	print "<body>"
	print "<h2>MTA Quiz</h2><FORM ACTION=mapquiz.cgi METHOD=POST><OL>"
	c = 0.0011
	
	#get numQuestions amout of questions
	for i in range(0,numQuestions):
		print 'Question '+str(i+1)
		#get the station name
		station_name = correct_names[i].split(',')[0]
		print "<p><li><b>" + 'Which line stops at '+station_name+'?'
		#get the coordinates for web presentation
		longitude =  coordinates[i][0]
		latitude =   coordinates[i][1]
		long_minus_c =  float(longitude) - c
		lati_minus_c =  float(latitude) - c
		long_plus_c  = float(longitude) + c
		lati_plus_c =  float(latitude) + c
		
		#put correct answer and (numChoices - 1) number of wrong answers
		choices = []
		random.shuffle(correct_route_lists[i])
		answer = correct_route_lists[i][0]
		choices.append(answer)
		random.shuffle(wrong_route_lists[i])
		for j in range(0,numChoices - 1):
			choices.append(wrong_route_lists[i][j])
		random.shuffle(choices)
		
		#show map
		print "<p>"
		print '<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"'+'src="http://www.openstreetmap.org/export/embed.html?bbox='
		print str(lati_minus_c)+','+str(long_minus_c)+','+str(lati_plus_c)+','+str(long_plus_c)+'&layer=hot&marker='+str(longitude)+','+str(latitude)+'"'+'style="border: 1px solid black"></iframe>'
		print "<p>"

		#show choices
		for j in range(0, numChoices):
			print "<input type=radio name=q"+str(i)+" value="+choices[j]+">"+choices[j]+"<br>"
		print "</li>"
		
print "</OL><INPUT TYPE=SUBMIT ></FORM>"
print "</body>"
print "</html>"

if os.environ['REQUEST_METHOD'] == 'POST':
	num_Correct = 0
	num_Wrong = 0
	correctAnswers = []
	wrongAnswers = []
	for i in range(0, numQuestions):
		if form["q"+str(i)].value in correct_route_lists[i]:
			num_Correct += 1
			correctAnswers.append(name_list[i])
		else:
			num_Wrong += 1
			wrongAnswers.append(name_list[i])

	print "<html>"
	print "<body>"
	
	percentage = (num_Correct * 100)/(num_Correct+num_Wrong)
	print "<h2>Your Score: " + str(percentage) +'%</h2>'

	print "<h3>Correct</h3>"
	print "<td valign=top><font color=green>"
	for i in range(0, len(correctAnswers)):
		print correctAnswers[i] + " <br>"
	print "</font></td>"
	
	
	print "<h3>Incorrect</h3>"
	print "<td valign=top><font color=red>"
	for j in range(0, len(wrongAnswers)):
		print wrongAnswers[j] + " <br>"
	print "</font></td>"
	
	print "</body>"
	print "</html>"
	