#! /usr/bin/python
# Tianhui Zhu
# N18846520
# tz406@nyu.edu
# http://cims.nyu.edu/~tz406/cgi-bin/mapquiz.cgi
import random
import os
import cgi, cgitb

cgitb.enable()
form = cgi.FieldStorage()

f = open('/web/tz406/cgi-bin/StationEntrances.csv', 'r')
allLines = f.readlines()
f.close()
input_length = len(allLines)

numQuestions, numChoices = 5, 4
dic = {}
name_set, route_set = set(), set()
routes, correct_names, correct_route_lists, wrong_route_lists, coordinates, name_list, route_list = [],[],[],[],[],[],[]

def createDict(length):
	# create dictionary from all lines
	for i in range(1, length):
		list = allLines[i].split(',')
		content = []
		name = list[1] + ',' + list[2]
		name_set.add(name)
		content.append(list[3])
		content.append(list[4])
		for i in range(5, 16):
			if list[i] != '':
				content.append(list[i])
		for i in range(6, 16):
			route_set.add(list[i])
		dic[name] = content
		
# get list from set
#?? list = list(set) does not work, why?
def createSets(name_set, route_set):
	for i in name_set:
		if i != '':
			name_list.append(i)
	random.shuffle(name_list)
	for i in route_set:
		if i != '':
			route_list.append(i)

#create questions, answer and wrong choices
def createQA(numQuestions):
	# create choice
	for i in range(0, numQuestions):
		# choose one name in the name_list as correct answer
		name = name_list[i]
		correct_names.append(name)
		# get the coordinates of this station
		coordinate = []
		coordinate.append(dic[name][0])
		coordinate.append(dic[name][1])
		coordinates.append(coordinate)
		# get all the possible correct routes at this station
		correct_route_list = []
		for i in range(2, len(dic[name])):
			correct_route_list.append(dic[name][i])
		# get all the possible wrong routes at this station
		wrong_route_set = route_set - set(correct_route_list)
		wrong_route_list = []
		for i in wrong_route_set:
			if i != '':
				wrong_route_list.append(i)
		wrong_route_lists.append(wrong_route_list)
		correct_route_lists.append(correct_route_list)

# create the quiz page
def createQPage():
	# default web page
	print "Content-type:text/html\n\n"
	if os.environ['REQUEST_METHOD'] == 'GET':
		c = 0.0011
		print "<html>"
		print "<body>"
		print "<h2>MTA Quiz</h2><FORM ACTION=mapquiz.cgi METHOD=POST><OL>"
		# get numQuestions amout of questions
		for i in range(0, numQuestions):
			print "<h3>Question " + str(i + 1) + "</h3>"
			# get the station name
			station_name = correct_names[i].split(',')[1]
			print "<p><b>" + 'Which line stops at ' + station_name + '?'
			# get the coordinates for web presentation
			longitude = coordinates[i][0]
			latitude = coordinates[i][1]
			long_minus_c, lati_minus_c, long_plus_c, lati_plus_c\
				= float(longitude) - c, float(latitude) - c, float(longitude) + c, float(latitude) + c
			# put correct answer and (numChoices - 1) number of wrong answers
			choices = []
			random.shuffle(correct_route_lists[i])
			answer = correct_route_lists[i][0]
			#print answer
			# print correct_route_lists[i]
			choices.append(answer)
			random.shuffle(wrong_route_lists[i])
			for j in range(0, numChoices - 1):
				choices.append(wrong_route_lists[i][j])
			random.shuffle(choices)
			answer_index = choices.index(answer)
			# show map
			print "<p>"
			print '<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"'' \
			''src="http://www.openstreetmap.org/export/embed.html?bbox=' + \
				  str(lati_minus_c) + ',' + str(long_minus_c) + ',' + str(lati_plus_c) + ',' + str(long_plus_c) + \
				  '&layer=hot&marker=' + str(longitude) + ',' + str(latitude) + '"' \
				  + 'style="border: 1px solid black"></iframe>'
			print "<p>"
			# show choices
			print "<input type=hidden name=a" + str(i) + " value=" + str(answer_index) + ">"
			print "<tr><td><input type=hidden name=s" + str(i) + " value=" + '"' + station_name + '"' + "></td></tr>"
			# print station_name
			for j in range(0, numChoices):
				print "<input type=radio name=q" + str(i) + " value=" + str(j) + ">" + choices[j]
		print "</OL><INPUT TYPE=SUBMIT></FORM>"
		print "</body>"
		print "</html>"


def createResult():
	if os.environ['REQUEST_METHOD'] == 'POST':
		num_Correct = 0
		num_Wrong = 0
		correctAnswers = []
		wrongAnswers = []
		
		for i in range(0, numQuestions):
			# I know this looks very 'brute' here using try catch this wa y
			# but using try catch exception is indeed a way to program
			# simply because here using radio there is no other type exception
			# love this idea
			# print "times"
			try:
				# == vs is
				if form["q" + str(i)].value == form["a" + str(i)].value:
					num_Correct += 1
					correctAnswers.append(form["s" + str(i)].value)
				else:
					num_Wrong += 1
					wrongAnswers.append(form["s" + str(i)].value)
			except:
				num_Wrong += 1
				wrongAnswers.append(form["s" + str(i)].value)
				# continue
		print "<html>"
		print "<body>"
		percentage = (num_Correct * 100) / (num_Correct + num_Wrong)
		print "<h2>Your Score: " + str(percentage) + '%</h2>'
		print "<h3>Correct</h3>"
		print "<td valign=top><font color=green>"
		for i in range(0, num_Correct):
			print correctAnswers[i] + " <br>"
		print "</font></td>"
		print "<h3>Incorrect</h3>"
		print "<td valign=top><font color=red>"
		for j in range(0, num_Wrong):
			print wrongAnswers[j] + " <br>"
		print "</font></td>"
		print "</body>"
		print "</html>"


createDict(input_length)
createSets(name_set, route_set)
createQA(numQuestions)
createQPage()
createResult()